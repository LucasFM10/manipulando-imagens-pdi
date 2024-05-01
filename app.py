import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

# comentário inútil
def carregar_imagem():
    # Define os tipos de arquivo para a caixa de diálogo
    tipos_de_arquivo = [
        ("Todos os arquivos de imagem", "*.jpeg *.jpg *.png *.gif *.bmp"),
        ("JPEG", "*.jpeg"),
        ("JPEG", "*.jpg"),
        ("PNG", "*.png"),
        ("GIF", "*.gif"),
        ("BMP", "*.bmp"),
        ("Todos os arquivos", "*.*")
    ]

    # Abrir a caixa de diálogo para selecionar a imagem, especificando os tipos de arquivo
    filepath = filedialog.askopenfilename(filetypes=tipos_de_arquivo, initialdir='/home/lucas/Downloads')
    
    # Verifica se um caminho de arquivo foi selecionado
    if filepath:
        # Carrega a imagem usando PIL
        global imagem_atual  # Define a imagem carregada como uma variável global para acesso em outras funções
        imagem_atual = Image.open(filepath)
        
        # Redimensiona a imagem para se ajustar à tela, se necessário
        imagem_atual = imagem_atual.resize((500, 500), Image.Resampling.LANCZOS)
        
        # Atualiza a exibição da imagem
        atualizar_imagem(imagem_atual)

    
    # Cria o botão para inverter as cores da imagem
    botao_inverter = tk.Button(frame_botoes, text="Inverter Cores", command=inverter_cores)
    botao_inverter.pack(side=tk.RIGHT, expand=True, padx=10)


    # Slider para ajuste de contraste
    slider_contraste = tk.Scale(frame_botoes, from_=-1, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Contraste", command=print("aaaa"))
    slider_contraste.set(1.0)  # Valor padrão de contraste é 1 (sem alteração)
    slider_contraste.pack(side=tk.RIGHT, expand=True, padx=10)

def inverter_cores():
    global imagem_atual
    if imagem_atual:  # Verifica se a imagem foi carregada
                # Converte a imagem para o modo "RGB" para garantir compatibilidade
        imagem_atual = imagem_atual.convert("RGB")
        pixels = imagem_atual.load()  # Carrega os dados dos pixels da imagem

        # Obtem as dimensões da imagem
        largura, altura = imagem_atual.size

        # Itera sobre cada pixel da imagem
        for x in range(largura):
            for y in range(altura):
                r, g, b = pixels[x, y]  # Obtem os valores de vermelho, verde e azul do pixel
                # Inverte os valores dos canais
                pixels[x, y] = (255 - r, 255 - g, 255 - b)

        # Atualiza a exibição da imagem com a imagem de cores invertidas
        atualizar_imagem(imagem_atual)
def atualizar_imagem(imagem):
    foto = ImageTk.PhotoImage(imagem)
    label_imagem.config(image=foto)
    label_imagem.image = foto  # Mantém uma referência!
    label_imagem.pack(pady=(0, 10))

# Cria a janela principal
root = tk.Tk()
root.geometry("600x700")

# Cria um Frame como contêiner para os botões
frame_botoes = tk.Frame(root, width=600, height=100)
frame_botoes.pack_propagate(False)
frame_botoes.pack(pady=20)

# Cria o botão para carregar a imagem
botao_carregar = tk.Button(frame_botoes, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.pack(side=tk.LEFT, expand=True, padx=10)

# Label para mostrar a imagem
label_imagem = tk.Label(root)

# Inicia o loop principal
root.mainloop()
