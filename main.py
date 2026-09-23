import tkinter as tk
from tkinter import messagebox, ttk

LINHAS = 5
COLUNAS = 6
TOTAL_POSICOES = LINHAS * COLUNAS

ocupacao = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]
identificacoes = [['' for _ in range(COLUNAS)] for _ in range(LINHAS)]
botoes = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
janela = None
entrada_codigo = None
resumo_var = None
total_chegadas = 0

def codigo_da_posicao(linha, coluna):
    return f'P{linha + 1}{coluna + 1}'


def contar_ocupadas():
    total = 0
    # Dois loops percorrem a matriz como faria um algoritmo tradicional de contagem.
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            total += ocupacao[linha][coluna]
    return total


def codigo_ja_registrado(codigo):
    # A busca sequencial visita cada célula até encontrar o código informado.
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if identificacoes[linha][coluna] == codigo:
                return True
    return False


def atualizar_botao(linha, coluna):
    botao = botoes[linha][coluna]
    if ocupacao[linha][coluna] == 1:
        # get lê uma posição da matriz; configure atualiza o widget nativo.
        botao.configure(text=identificacoes[linha][coluna], style='Ocupado.TButton')
    else:
        botao.configure(text=codigo_da_posicao(linha, coluna), style='Livre.TButton')


def atualizar_resumo():
    ocupadas = contar_ocupadas()
    livres = TOTAL_POSICOES - ocupadas
    # set substitui o texto de um StringVar ligado ao Label de resumo.
    resumo_var.set(f'Livres: {livres}  |  Ocupadas: {ocupadas}  |  Chegadas: {total_chegadas}')


def registrar_chegada(linha, coluna):
    global total_chegadas
    codigo = entrada_codigo.get().strip().upper()
    # strip remove espaços externos e upper padroniza a identificação.
    if codigo == '':
        messagebox.showwarning('Validação', 'Informe a identificação do contêiner.')
        return
    if codigo_ja_registrado(codigo):
        messagebox.showwarning('Validação', 'Essa identificação já está no pátio.')
        return
    ocupacao[linha][coluna] = 1
    identificacoes[linha][coluna] = codigo
    total_chegadas += 1
    entrada_codigo.delete(0, tk.END)
    atualizar_botao(linha, coluna)
    atualizar_resumo()


def registrar_saida(linha, coluna):
    codigo = identificacoes[linha][coluna]
    # askyesno pausa o fluxo e só confirma a saída quando o usuário responde sim.
    confirmar = messagebox.askyesno('Confirmar saída', f'Retirar o contêiner {codigo}?')
    if not confirmar:
        return
    ocupacao[linha][coluna] = 0
    identificacoes[linha][coluna] = ''
    atualizar_botao(linha, coluna)
    atualizar_resumo()


def clicar_posicao(linha, coluna):
    if ocupacao[linha][coluna] == 0:
        registrar_chegada(linha, coluna)
    else:
        registrar_saida(linha, coluna)


def criar_acao_da_posicao(linha, coluna):
    # A função retorna outra função para guardar linha e coluna no comando do botão.
    def acao():
        clicar_posicao(linha, coluna)
    return acao


def montar_lista_de_ocupacao(painel):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            botao = ttk.Button(
                painel,
                text=codigo_da_posicao(linha, coluna),
                command=criar_acao_da_posicao(linha, coluna),
                style='Livre.TButton',
                width=10,
            )
            # grid posiciona os 30 botões na tabela visual do pátio.
            botao.grid(row=linha, column=coluna, padx=4, pady=4, sticky='nsew')
            botoes[linha][coluna] = botao
    for coluna in range(COLUNAS):
        painel.columnconfigure(coluna, weight=1)


def encerrar():
    ocupadas = contar_ocupadas()
    livres = TOTAL_POSICOES - ocupadas
    lista = []
    # append acrescenta cada item à lista, operação equivalente à inserção sequencial.
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if ocupacao[linha][coluna] == 1:
                lista.append(f'{codigo_da_posicao(linha, coluna)}: {identificacoes[linha][coluna]}')
    detalhes = '\n'.join(lista) if lista else 'Nenhum contêiner no pátio.'
    messagebox.showinfo(
        'Resumo final',
        f'Posições livres: {livres}\nPosições ocupadas: {ocupadas}\n\n{detalhes}',
    )
    # destroy encerra a janela principal depois do resumo final.
    janela.destroy()


def montar_interface():
    global janela, entrada_codigo, resumo_var
    janela = tk.Tk()
    janela.title('Controle de Contêineres')
    janela.resizable(False, False)

    estilo = ttk.Style()
    # theme_use seleciona um tema nativo disponível no ttk.
    estilo.theme_use('clam')
    estilo.configure('Livre.TButton', padding=8)
    estilo.configure('Ocupado.TButton', padding=8)

    cabecalho = ttk.Frame(janela, padding=12)
    # pack organiza o cabeçalho e mantém o código simples.
    cabecalho.pack(fill='x')
    ttk.Label(cabecalho, text='Identificação do contêiner:').grid(row=0, column=0, padx=(0, 8))
    entrada_codigo = ttk.Entry(cabecalho, width=24)
    entrada_codigo.grid(row=0, column=1, padx=(0, 8))
    ttk.Label(cabecalho, text='Clique em uma posição para chegada ou saída.').grid(row=1, column=0, columnspan=2, pady=(8, 0))

    quadro_patio = ttk.LabelFrame(janela, text='Pátio 5 x 6', padding=12)
    quadro_patio.pack(fill='both', padx=12, pady=(0, 12))
    montar_lista_de_ocupacao(quadro_patio)

    resumo_var = tk.StringVar(value='')
    ttk.Label(janela, textvariable=resumo_var).pack(pady=(0, 8))
    atualizar_resumo()

    rodape = ttk.Frame(janela, padding=(12, 0, 12, 12))
    rodape.pack(fill='x')
    ttk.Button(rodape, text='Encerrar e mostrar resumo', command=encerrar).pack(side='right')


def iniciar_aplicacao():
    montar_interface()
    # mainloop mantém a interface respondendo aos eventos de clique.
    janela.mainloop()


if __name__ == '__main__':
    iniciar_aplicacao()
