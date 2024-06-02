
import tiktoken
import torch
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
from dataseMaker import GPTDatasetV1
from model import GPTModel

class FederatedLearning:
    def __init__(self, df_path, train_ratio, checkpoint_path):
        self.df_path = df_path
        self.train_ratio = train_ratio
        self.checkpoint_path = checkpoint_path
        
        
    def create_dataloader_v1(self, txt, batch_size=4, max_length=256, stride=128, shuffle=True, drop_last=True):
        tokenizer = tiktoken.get_encoding("gpt2")
        dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last)
        return dataloader
    
        
    def calc_loss_batch(self, input_batch, target_batch, model, device):
        input_batch, target_batch = input_batch.to(device), target_batch.to(device)
        logits = model(input_batch)
        loss = torch.nn.functional.cross_entropy(
            logits.flatten(0, 1), target_batch.flatten()
        )
        return loss
        
    def calc_loss_loader(self, data_loader, model, device, num_batches=None):
        total_loss = 0.
        if num_batches is None:
            num_batches = len(data_loader)
        else:
            num_batches = min(num_batches, len(data_loader))
        for i, (input_batch, target_batch) in enumerate(data_loader):
            if i < num_batches:
                loss = self.calc_loss_batch(input_batch, target_batch, model, device)
                total_loss += loss.item()
            else:
                break
        return total_loss / num_batches
    
    
    
    
    def evaluate_model(self, model, train_loader, val_loader, device, eval_iter):
        model.eval()
        with torch.no_grad():
            train_loss = self.calc_loss_loader(train_loader, model, device, num_batches=eval_iter)
            val_loss = self.calc_loss_loader(val_loader, model, device, num_batches=eval_iter)
        model.train()
        return train_loss, val_loss
    
    def text_to_token_ids(self, text, tokenizer):
        encoded = tokenizer.encode(text, allowed_special={'<|endoftext|>'})
        encoded_tensor = torch.tensor(encoded).unsqueeze(0) # add batch dimension
        return encoded_tensor

    def token_ids_to_text(self, token_ids, tokenizer):
        flat = token_ids.squeeze(0) # remove batch dimension
        return tokenizer.decode(flat.tolist())
    def generate(self, model, idx, max_new_tokens, context_size, temperature, top_k=None):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -context_size:]
            with torch.no_grad():
                logits = model(idx_cond)
            logits = logits[:, -1, :]
            if top_k is not None:
                top_logits, _ = torch.topk(logits, top_k)
                min_val = top_logits[:, -1]
                logits = torch.where(
                    logits < min_val,
                    torch.tensor(float('-inf')).to(logits.device),
                    logits
                )
            if temperature > 0.0:
                logits = logits / temperature
                probs = torch.softmax(logits, dim=-1)
                idx_next = torch.multinomial(probs, num_samples=1)
            else:
                idx_next = torch.argmax(logits, dim=-1, keepdim=True)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
    
    def generate_and_print_sample(self, model, tokenizer, device, start_context):
        model.eval()
        context_size = model.pos_emb.weight.shape[0]
        encoded = self.text_to_token_ids(start_context, tokenizer).to(device)
        with torch.no_grad():
            token_ids = self.generate(
                model=model, idx=encoded,
                max_new_tokens=50, context_size=context_size,
                top_k=25,
                temperature=1.4
            )
            decoded_text = self.token_ids_to_text(token_ids, tokenizer)
            print(decoded_text.replace("\n", " "))  # Compact print format
        model.train()
    
    def generate_and_print_sample(self, model, tokenizer, device, start_context):
        model.eval()
        context_size = model.pos_emb.weight.shape[0]
        encoded = self.text_to_token_ids(start_context, tokenizer).to(device)
        with torch.no_grad():
            token_ids = self.generate(
                model=model, idx=encoded,
                max_new_tokens=50, context_size=context_size,
                top_k=25,
                temperature=1.4
            )
            decoded_text = self.token_ids_to_text(token_ids, tokenizer)
            print(decoded_text.replace("\n", " "))  # Compact print format
        model.train()
        
    def train_model_simple(self, model, train_loader, val_loader, optimizer, device, num_epochs, eval_freq, eval_iter, start_context):
        train_losses, val_losses, track_tokens_seen = [], [], []
        tokens_seen, global_step = 0, -1

        for epoch in range(num_epochs):
            model.train()
            for input_batch, target_batch in train_loader:
                optimizer.zero_grad()
                loss = self.calc_loss_batch(input_batch, target_batch, model, device)
                loss.backward()
                optimizer.step()
                tokens_seen += input_batch.numel()
                global_step += 1

                if global_step % eval_freq == 0:
                    train_loss, val_loss = self.evaluate_model(
                        model, train_loader, val_loader, device, eval_iter)
                    train_losses.append(train_loss)
                    val_losses.append(val_loss)
                    track_tokens_seen.append(tokens_seen)
                    print(f"Ep {epoch+1} (Step {global_step:06d}): "
                          f"Train loss {train_loss:.3f}, Val loss {val_loss:.3f}")

            self.generate_and_print_sample(
                model, train_loader.dataset.tokenizer, device, start_context
            )
        return train_losses, val_losses, track_tokens_seen

    def start_train(self, num_epochs):
        with open(self.df_path) as f:
            text = f.read()
        
        split_idx = int(self.train_ratio * len(text))
        train_data = text[:split_idx]
        val_data = text[split_idx:]
        
        train_loader = self.create_dataloader_v1(
            train_data,
            batch_size=2,
        )
        val_loader = self.create_dataloader_v1(
            val_data,
            batch_size=2,
        )
        
        GPT_CONFIG_124M = {
            'vocab_size': 50257,   # Vucabulary Size
            'ctx_len': 1024,       # Context Lenghts
            'emb_dim': 768,        # Embedding dimennsion
            'n_heads': 12,         # Number of attention head
            'n_layers': 12,        # number of Layer
            'drop_rate': 0.1,      # Dropout rate
            'qkv_bias': False      # Query_Key_value Bias
        }

        model = GPTModel(GPT_CONFIG_124M)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        if torch.cuda.is_available():
            checkpoint = torch.load(self.checkpoint_path)
        else:
            checkpoint = torch.load(self.checkpoint_path, map_location=torch.device('cpu'))
            
        model.load_state_dict(checkpoint["model_state_dict"])
        opt = optim.Adam(model.parameters(), lr=0.1)
        
        
        
        train_losses, val_losses, tokens_seen = self.train_model_simple(
            model, train_loader, val_loader, opt, device,
            num_epochs=num_epochs, eval_freq=5, eval_iter=1,
            start_context="Every effort moves you"
        )

        return model
        
