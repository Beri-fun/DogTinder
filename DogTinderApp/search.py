from PIL import Image
import joblib
import torch
import torchvision.transforms as transforms
import torchvision.models as models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_embedding(img_path, transform, resnet):
    img = Image.open(img_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = resnet(tensor).cpu().numpy().flatten()
    return emb

def serach_for_similar_image(query):

    nn, paths, _ = joblib.load("DogTinderApp/sklearn_index.pkl")
    top_k=5

    resnet = models.resnet50(weights=True)
    resnet.fc = torch.nn.Identity()
    resnet.eval()
    resnet = resnet.to(device)

    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    query_emb = get_embedding(query, transform, resnet).reshape(1,-1)
    distances, indices = nn.kneighbors(query_emb, n_neighbors=top_k)
    results = [(paths[idx], 1 - dist) for idx, dist in zip(indices[0], distances[0])]
    return results[1][0]
