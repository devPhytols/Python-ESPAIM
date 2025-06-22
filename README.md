# AssaultCube ESP (Educational)

Este projeto é um simples **ESP (Extra Sensory Perception)** para o jogo **AssaultCube**, desenvolvido com fins puramente educacionais. O código demonstra como ler a memória de um processo e renderizar informações na tela, como caixas ao redor dos jogadores, barras de vida e linhas de snap (snaplines).

⚠️ **Aviso:** Este código é apenas para estudo sobre leitura de memória e sobreposição gráfica. Não utilize em ambientes online ou para obter vantagem desleal em jogos. O uso indevido pode violar os termos de serviço do jogo.

## ✨ Funcionalidades

- Exibe caixas (ESP boxes) ao redor de jogadores.
- Mostra o nome, vida e distância de cada jogador.
- Snapline (linha) do centro da tela até os inimigos.
- Barra de saúde dinâmica.
- Diferenciação por cor:
  - 🟥 Inimigos em vermelho
  - 🟩 Aliados em verde

## 📦 Requisitos

- **Python 3.9+**
- [pymem](https://pypi.org/project/pymem/)
- [pyray](https://pypi.org/project/pyray/)
- Dependências adicionais: `helper.py`.

## 🛠 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/assaultcube-esp.git
cd assaultcube-esp
```

Instale os pacotes necessários:

```bash
pip install pymem pyray
```

## 🚀 Como usar

1 - Abra o Jogo.
2 - Execute o script:

```bash
python esp.py
```

## 📌 Observações

- É necessário ter o helper.py com:
- Offsets (Atualizados).
- Estruturas (Entity, Vec3).
- Função world_to_screen.

## 📄 Licença 
Distribuído sob a licença MIT.
