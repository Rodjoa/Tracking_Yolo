import torch

print("Torch version:", torch.__version__)
print("CUDA disponible:", torch.cuda.is_available())
print("GPU detectada:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NINGUNA")