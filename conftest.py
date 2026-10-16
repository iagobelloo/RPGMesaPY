import os
import glob
import pytest

@pytest.fixture(autouse=True, scope="session")
def protect_user_saves():
    """
    Protege integralmente os arquivos de save do jogador durante a execucao
    de suites de testes automatizados com pytest.
    Faz backup no inicio da sessao de testes e restaura perfeitamente ao final,
    apagando quaisquer saves 'falsos' criados por testes unitarios.
    """
    saves_dir = "saves"
    backup = {}
    if os.path.exists(saves_dir):
        for p in glob.glob(os.path.join(saves_dir, "*")):
            if os.path.isfile(p) and not p.endswith(".gitkeep"):
                with open(p, "rb") as f:
                    backup[os.path.basename(p)] = f.read()

    yield

    if os.path.exists(saves_dir):
        # Remove arquivos temporários de teste gerados durante a suíte
        for p in glob.glob(os.path.join(saves_dir, "*")):
            if os.path.isfile(p) and not p.endswith(".gitkeep"):
                fname = os.path.basename(p)
                if fname not in backup:
                    try:
                        os.remove(p)
                    except Exception:
                        pass
        # Restaura os arquivos originais que existiam antes dos testes
        for fname, content in backup.items():
            dest = os.path.join(saves_dir, fname)
            try:
                with open(dest, "wb") as f:
                    f.write(content)
            except Exception:
                pass

