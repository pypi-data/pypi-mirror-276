import kagglehub
from federated.trainer import FederatedLearning



# Download latest version
path = kagglehub.model_download("golammostofas/mr.x/pyTorch/1.0.0")



df_path = 'federated/wizard_of_zo.txt'
checkpoint_path = f'{path}/model_and_optimizer.pth'
train_ratio = 0.9
ob = FederatedLearning(df_path=df_path, checkpoint_path=checkpoint_path, train_ratio=train_ratio)

model = ob.start_train(2)