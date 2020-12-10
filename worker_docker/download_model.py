from torchvision import models
# get the model
model = models.vgg16(pretrained=True).eval()