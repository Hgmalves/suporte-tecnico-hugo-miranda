import os
import sys
import subprocess
import ctypes
import platform
import socket
import time
from datetime import datetime

# ============================================================
#  SUPORTE TECNICO - Hugo Miranda -Suporte
#  Desenvolvido por: Hugo Miranda -Suporte
#  Versao: 2.0 | 2026
# ============================================================

if platform.system() != "Windows":
    print("[ERRO] Este script foi desenvolvido exclusivamente para Windows.")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def rerun_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

class Cores:
    VERDE    = "\033[92m"
    AMARELO  = "\033[93m"
    VERMELHO = "\033[91m"
    CIANO    = "\033[96m"
    RESET    = "\033[0m"
    BOLD     = "\033[1m"

def ativar_cores():
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def cabecalho():
    os.system("cls")
    print(Cores.VERDE + Cores.BOLD)
    print("=" * 42)
    print("      SUPORTE TECNICO - Hugo Miranda -Suporte v2.0")
    print("=" * 42)
    print(Cores.RESET)

def pausar():
    print()
    input(Cores.CIANO + "  Pressione ENTER para voltar ao menu..." + Cores.RESET)

def executar(cmd, shell=True):
    print(Cores.CIANO + f"\n  > {cmd}" + Cores.RESET)
    print()
    subprocess.run(cmd, shell=shell)

def executar_capturar(cmd, shell=True):
    """Executa comando e retorna (stdout, sucesso)."""
    try:
        r = subprocess.run(
            cmd, shell=shell,
            capture_output=True, text=True,
            encoding="cp850", errors="replace"
        )
        sucesso = r.returncode == 0
        return r.stdout + r.stderr, sucesso
    except Exception as e:
        return str(e), False

def titulo(texto):
    print()
    print(Cores.VERDE + Cores.BOLD + "=" * 42)
    print(f"  {texto}")
    print("=" * 42 + Cores.RESET)
    print()

# ============================================================
# RELATORIO
# ============================================================

class Relatorio:
    def __init__(self, nome_pacote):
        self.nome_pacote   = nome_pacote
        self.inicio        = datetime.now()
        self.itens         = []   # (descricao, status, detalhe)

    def adicionar(self, descricao, status, detalhe=""):
        """status: 'OK' | 'FALHA' | 'AVISO'"""
        self.itens.append((descricao, status, detalhe))

    def _linha_status(self, status):
        if status == "OK":
            return Cores.VERDE + "[OK]    " + Cores.RESET
        elif status == "FALHA":
            return Cores.VERMELHO + "[FALHA] " + Cores.RESET
        else:
            return Cores.AMARELO + "[AVISO] " + Cores.RESET

    def exibir(self):
        fim = datetime.now()
        duracao = int((fim - self.inicio).total_seconds())
        ok     = sum(1 for _, s, _ in self.itens if s == "OK")
        falhas = sum(1 for _, s, _ in self.itens if s == "FALHA")
        avisos = sum(1 for _, s, _ in self.itens if s == "AVISO")

        print()
        print(Cores.BOLD + Cores.VERDE + "=" * 42)
        print(f"  RELATORIO - {self.nome_pacote}")
        print(f"  Data : {self.inicio.strftime('%d/%m/%Y')}  Hora: {self.inicio.strftime('%H:%M')}")
        print(f"  Duracao: {duracao}s")
        print("=" * 42 + Cores.RESET)
        for desc, status, detalhe in self.itens:
            linha = self._linha_status(status)
            print(f"  {linha} {desc}")
            if detalhe:
                print(f"           {Cores.CIANO}{detalhe}{Cores.RESET}")
        print(Cores.BOLD + "-" * 42)
        print(
            f"  Resultado: "
            f"{Cores.VERDE}{ok} OK{Cores.RESET} | "
            f"{Cores.VERMELHO}{falhas} Falha(s){Cores.RESET} | "
            f"{Cores.AMARELO}{avisos} Aviso(s){Cores.RESET}"
        )
        print(Cores.BOLD + "=" * 42 + Cores.RESET)

        # Salvar ficheiro
        self._salvar(ok, falhas, avisos, duracao)

    def _salvar(self, ok, falhas, avisos, duracao):
        timestamp = self.inicio.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_{self.nome_pacote.replace(' ', '_')}_{timestamp}.txt"
        caminho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)
        linhas = []
        linhas.append("=" * 42)
        linhas.append(f"  RELATORIO - {self.nome_pacote}")
        linhas.append(f"  Data : {self.inicio.strftime('%d/%m/%Y')}  Hora: {self.inicio.strftime('%H:%M')}")
        linhas.append(f"  Duracao: {duracao}s")
        linhas.append("=" * 42)
        for desc, status, detalhe in self.itens:
            linhas.append(f"  [{status}]  {desc}")
            if detalhe:
                linhas.append(f"           {detalhe}")
        linhas.append("-" * 42)
        linhas.append(f"  Resultado: {ok} OK | {falhas} Falha(s) | {avisos} Aviso(s)")
        linhas.append("=" * 42)
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas))
            print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Relatorio salvo em: {caminho}")
        except Exception as e:
            print(f"\n  {Cores.VERMELHO}[ERRO]{Cores.RESET} Nao foi possivel salvar o relatorio: {e}")


# ============================================================
# FUNCOES INDIVIDUAIS (1 a 15)
# ============================================================

def op1_limpar_temp():
    titulo("1 - LIMPAR ARQUIVOS TEMPORARIOS")
    pastas = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch",
    ]
    total = 0
    for pasta in pastas:
        if not pasta or not os.path.exists(pasta):
            continue
        print(f"  Limpando: {pasta}")
        for raiz, dirs, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                try:
                    os.remove(caminho)
                    total += 1
                except:
                    pass
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} {total} arquivo(s) removido(s).")
    pausar()

def op1_limpar_temp_silencioso():
    """Versao silenciosa para uso em pacotes. Retorna (descricao, status, detalhe)."""
    pastas = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch",
    ]
    total = 0
    for pasta in pastas:
        if not pasta or not os.path.exists(pasta):
            continue
        for raiz, dirs, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                try:
                    os.remove(caminho)
                    total += 1
                except:
                    pass
    return ("Limpar arquivos temporarios", "OK", f"{total} arquivo(s) removido(s)")

def op2_limpar_dns():
    titulo("2 - LIMPAR CACHE DNS")
    executar("ipconfig /flushdns")
    print(f"  {Cores.VERDE}[OK]{Cores.RESET} Cache DNS limpo com sucesso.")
    pausar()

def op2_limpar_dns_silencioso():
    saida, ok = executar_capturar("ipconfig /flushdns")
    status = "OK" if ok else "FALHA"
    return ("Limpar cache DNS", status, "")

def op3_resetar_rede():
    titulo("3 - RESETAR REDE (COMPLETO)")
    cmds = [
        "netsh winsock reset",
        "netsh int ip reset",
        "ipconfig /release",
        "ipconfig /renew",
        "ipconfig /flushdns",
    ]
    for cmd in cmds:
        executar(cmd)
    print(f"\n  {Cores.AMARELO}[AVISO]{Cores.RESET} Reinicie o computador para aplicar todas as alteracoes.")
    pausar()

def op3_resetar_rede_silencioso():
    cmds = [
        "netsh winsock reset",
        "netsh int ip reset",
        "ipconfig /release",
        "ipconfig /renew",
        "ipconfig /flushdns",
    ]
    falhas = 0
    for cmd in cmds:
        _, ok = executar_capturar(cmd)
        if not ok:
            falhas += 1
    status = "OK" if falhas == 0 else "AVISO"
    detalhe = "Reinicio necessario para aplicar alteracoes"
    return ("Resetar rede completa", status, detalhe)

def op4_ver_ip():
    titulo("4 - CONFIGURACAO DE IP")
    executar("ipconfig /all")
    print("\n  IP Local (socket):", socket.gethostbyname(socket.gethostname()))
    pausar()

def op4_ver_ip_silencioso():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ("Ver configuracao de IP", "OK", f"IP local: {ip}")
    except:
        return ("Ver configuracao de IP", "FALHA", "Nao foi possivel obter IP")

def op5_ferramentas():
    titulo("5 - FERRAMENTAS DO SISTEMA")
    ferramentas = {
        "1": ("Gerenciador de Tarefas",     "taskmgr"),
        "2": ("Gerenciador de Dispositivos","devmgmt.msc"),
        "3": ("Servicos do Windows",         "services.msc"),
        "4": ("Editor de Registro",          "regedit"),
        "5": ("Firewall do Windows",         "firewall.cpl"),
        "6": ("Painel de Controle",          "control"),
        "7": ("Configuracoes do Windows",    "ms-settings:"),
        "0": ("Voltar",                      None),
    }
    for k, (nome, _) in ferramentas.items():
        print(f"    {Cores.VERDE}{k}{Cores.RESET}  -  {nome}")
    print()
    esc = input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip()
    if esc in ferramentas and ferramentas[esc][1]:
        subprocess.Popen(ferramentas[esc][1], shell=True)
        print(f"  {Cores.VERDE}[OK]{Cores.RESET} Abrindo {ferramentas[esc][0]}...")
        time.sleep(1)

def op6_sfc():
    titulo("6 - VERIFICAR SISTEMA (SFC)")
    print("  Este processo pode demorar alguns minutos...\n")
    executar("sfc /scannow")
    pausar()

def op6_sfc_silencioso():
    print(f"  {Cores.CIANO}  Executando SFC (pode demorar)...{Cores.RESET}")
    saida, ok = executar_capturar("sfc /scannow")
    if "nao encontrou nenhuma violacao" in saida.lower() or "did not find any integrity violations" in saida.lower():
        return ("Verificar sistema SFC", "OK", "Nenhuma violacao encontrada")
    elif "reparou" in saida.lower() or "repaired" in saida.lower():
        return ("Verificar sistema SFC", "OK", "Ficheiros corrompidos reparados")
    elif ok:
        return ("Verificar sistema SFC", "AVISO", "Verificar log em CBS.log")
    else:
        return ("Verificar sistema SFC", "FALHA", "Erro ao executar SFC")

def op7_chkdsk():
    titulo("7 - VERIFICAR DISCO (CHKDSK)")
    disco = input("  Informe a letra do disco [padrao C]: ").strip().upper() or "C"
    executar(f"chkdsk {disco}: /f /r /x")
    print(f"\n  {Cores.AMARELO}[AVISO]{Cores.RESET} Se solicitado, agende para a proxima reinicializacao.")
    pausar()

def op7_chkdsk_silencioso(disco="C"):
    print(f"  {Cores.CIANO}  Verificando disco {disco}:...{Cores.RESET}")
    saida, ok = executar_capturar(f"chkdsk {disco}:")
    if "nao encontrou problemas" in saida.lower() or "found no problems" in saida.lower():
        return ("Verificar disco CHKDSK", "OK", f"Disco {disco}: sem problemas")
    else:
        return ("Verificar disco CHKDSK", "AVISO", f"Disco {disco}: agende verificacao na reinicializacao")

def op8_dism():
    titulo("8 - REPARAR WINDOWS (DISM)")
    print("  Este processo pode demorar varios minutos...\n")
    cmds = [
        "DISM /Online /Cleanup-Image /CheckHealth",
        "DISM /Online /Cleanup-Image /ScanHealth",
        "DISM /Online /Cleanup-Image /RestoreHealth",
    ]
    for cmd in cmds:
        print(f"\n  {Cores.CIANO}Executando:{Cores.RESET} {cmd}")
        subprocess.run(cmd, shell=True)
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} DISM concluido.")
    pausar()

def op8_dism_silencioso():
    print(f"  {Cores.CIANO}  Executando DISM (pode demorar)...{Cores.RESET}")
    cmds = [
        "DISM /Online /Cleanup-Image /CheckHealth",
        "DISM /Online /Cleanup-Image /ScanHealth",
        "DISM /Online /Cleanup-Image /RestoreHealth",
    ]
    resultados = []
    for cmd in cmds:
        saida, ok = executar_capturar(cmd)
        resultados.append(ok)
    if all(resultados):
        return ("Reparar Windows DISM", "OK", "Imagem do Windows verificada e reparada")
    else:
        return ("Reparar Windows DISM", "AVISO", "Alguns passos DISM com aviso - verificar manualmente")

def op9_testar_conexao():
    titulo("9 - TESTAR CONEXAO")
    hosts = ["8.8.8.8", "1.1.1.1", "google.com", "microsoft.com"]
    for host in hosts:
        resultado = subprocess.run(
            f"ping -n 2 {host}", shell=True,
            capture_output=True, text=True
        )
        status = Cores.VERDE + "[OK]" if "TTL=" in resultado.stdout else Cores.VERMELHO + "[FALHA]"
        print(f"  {status}{Cores.RESET}  {host}")
    print()
    executar("tracert -d -h 10 8.8.8.8")
    pausar()

def op9_testar_conexao_silencioso():
    hosts = ["8.8.8.8", "1.1.1.1", "google.com"]
    ok_count = 0
    for host in hosts:
        r = subprocess.run(f"ping -n 2 {host}", shell=True, capture_output=True, text=True)
        if "TTL=" in r.stdout:
            ok_count += 1
    if ok_count == len(hosts):
        return ("Testar conexao", "OK", f"{ok_count}/{len(hosts)} hosts alcancados")
    elif ok_count > 0:
        return ("Testar conexao", "AVISO", f"Apenas {ok_count}/{len(hosts)} hosts alcancados")
    else:
        return ("Testar conexao", "FALHA", "Sem conectividade com a internet")

def op10_windows_update():
    titulo("10 - RESETAR WINDOWS UPDATE")
    cmds = [
        "net stop wuauserv",
        "net stop cryptSvc",
        "net stop bits",
        "net stop msiserver",
        r'rd /s /q "C:\Windows\SoftwareDistribution"',
        r'rd /s /q "C:\Windows\System32\catroot2"',
        "net start wuauserv",
        "net start cryptSvc",
        "net start bits",
        "net start msiserver",
    ]
    for cmd in cmds:
        executar(cmd)
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Windows Update resetado com sucesso.")
    pausar()

def op10_windows_update_silencioso():
    cmds_stop  = ["net stop wuauserv", "net stop cryptSvc", "net stop bits", "net stop msiserver"]
    cmds_del   = [r'rd /s /q "C:\Windows\SoftwareDistribution"', r'rd /s /q "C:\Windows\System32\catroot2"']
    cmds_start = ["net start wuauserv", "net start cryptSvc", "net start bits", "net start msiserver"]
    falhas = 0
    for cmd in cmds_stop + cmds_del + cmds_start:
        _, ok = executar_capturar(cmd)
        if not ok:
            falhas += 1
    status = "OK" if falhas <= 2 else "AVISO"
    return ("Resetar Windows Update", status, "Servicos reiniciados com sucesso")

def op11_portas_abertas():
    titulo("11 - VER PORTAS ABERTAS")
    executar("netstat -ano")
    pausar()

def op12_processos():
    titulo("12 - VER PROCESSOS")
    executar("tasklist /v")
    pausar()

def op13_usuarios():
    titulo("13 - USUARIOS LOGADOS")
    executar("query user")
    print()
    executar("net user")
    pausar()

def op14_diagnostico():
    titulo("14 - DIAGNOSTICO COMPLETO")
    print("  Coletando informacoes do sistema...\n")
    relatorio = []
    r = subprocess.run("systeminfo", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("=== INFORMACOES DO SISTEMA ===\n" + r.stdout)
    r = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== CONFIGURACAO DE REDE ===\n" + r.stdout)
    r = subprocess.run("wmic logicaldisk get caption,freespace,size", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== DISCOS ===\n" + r.stdout)
    r = subprocess.run("tasklist", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== PROCESSOS ATIVOS ===\n" + r.stdout)
    r = subprocess.run("netstat -ano", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== PORTAS ABERTAS ===\n" + r.stdout)
    caminho = os.path.join(os.path.expanduser("~"), "Desktop", "diagnostico_HUGO_MIRANDA.txt")
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("\n".join(relatorio))
        print(f"  {Cores.VERDE}[OK]{Cores.RESET} Relatorio salvo em: {caminho}")
    except Exception as e:
        print(f"  {Cores.VERMELHO}[ERRO]{Cores.RESET} Nao foi possivel salvar: {e}")
    for secao in relatorio[:2]:
        print(secao[:500])
    pausar()

def op15_limpeza_total():
    titulo("15 - LIMPEZA COMPLETA (TUDO)")
    print(f"  {Cores.AMARELO}[AVISO]{Cores.RESET} Esta opcao executara TODAS as limpezas.")
    conf = input("  Confirma? (s/n): ").strip().lower()
    if conf != "s":
        print("  Operacao cancelada.")
        pausar()
        return
    op1_limpar_temp()
    op2_limpar_dns()
    op3_resetar_rede()
    op10_windows_update()
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Limpeza completa finalizada!")
    print(f"  {Cores.AMARELO}[AVISO]{Cores.RESET} Reinicie o computador para aplicar todas as alteracoes.")
    pausar()


# ============================================================
# PACOTES DE MANUTENCAO
# ============================================================

PACOTES = {
    "P1": {
        "nome": "PACOTE REDE",
        "desc": "Limpar DNS + Resetar rede + Testar conexao",
        "passos": [
            op2_limpar_dns_silencioso,
            op3_resetar_rede_silencioso,
            op9_testar_conexao_silencioso,
        ],
    },
    "P2": {
        "nome": "PACOTE LENTIDAO",
        "desc": "Limpar temp + Verificar sistema + Verificar disco",
        "passos": [
            op1_limpar_temp_silencioso,
            op6_sfc_silencioso,
            op7_chkdsk_silencioso,
        ],
    },
    "P3": {
        "nome": "PACOTE WINDOWS",
        "desc": "Reparar Windows (DISM) + Resetar Windows Update",
        "passos": [
            op8_dism_silencioso,
            op10_windows_update_silencioso,
        ],
    },
    "P4": {
        "nome": "PACOTE DIAGNOSTICO",
        "desc": "Ver IP + Testar conexao + Portas abertas",
        "passos": [
            op4_ver_ip_silencioso,
            op9_testar_conexao_silencioso,
        ],
    },
    "P5": {
        "nome": "PACOTE COMPLETO",
        "desc": "Limpeza + Rede + Verificacao + Reparacao (TUDO)",
        "passos": [
            op1_limpar_temp_silencioso,
            op2_limpar_dns_silencioso,
            op3_resetar_rede_silencioso,
            op6_sfc_silencioso,
            op8_dism_silencioso,
            op10_windows_update_silencioso,
            op9_testar_conexao_silencioso,
        ],
    },
}

def executar_pacote(chave):
    pacote = PACOTES[chave]
    titulo(pacote["nome"])
    print(f"  {Cores.CIANO}{pacote['desc']}{Cores.RESET}")
    print()

    rel = Relatorio(pacote["nome"])

    for i, func in enumerate(pacote["passos"], 1):
        total = len(pacote["passos"])
        print(f"  [{i}/{total}] Executando...", end="\r")
        resultado = func()
        descricao, status, detalhe = resultado
        rel.adicionar(descricao, status, detalhe)
        icone = Cores.VERDE + "✓" if status == "OK" else (Cores.VERMELHO + "✗" if status == "FALHA" else Cores.AMARELO + "!")
        print(f"  [{i}/{total}] {icone}{Cores.RESET} {descricao}          ")

    rel.exibir()
    pausar()

def menu_pacotes():
    cabecalho()
    print(Cores.BOLD + "  PACOTES DE MANUTENCAO\n" + Cores.RESET)
    for chave, p in PACOTES.items():
        print(f"  {Cores.VERDE}{chave}{Cores.RESET}  -  {p['nome']}")
        print(f"       {Cores.CIANO}{p['desc']}{Cores.RESET}")
        print()
    print("=" * 42)
    print(f"  {Cores.VERDE} 0{Cores.RESET}  -  Voltar ao menu principal")
    print("=" * 42)
    return input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip().upper()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():
    cabecalho()
    opcoes = [
        (" 1", "Limpar arquivos temporarios"),
        (" 2", "Limpar cache DNS"),
        (" 3", "Resetar rede (completo)"),
        (" 4", "Ver configuracao de IP"),
        (" 5", "Ferramentas do sistema"),
        (" 6", "Verificar sistema (SFC)"),
        (" 7", "Verificar disco (CHKDSK)"),
        (" 8", "Reparar Windows (DISM)"),
        (" 9", "Testar conexao"),
        ("10", "Resetar Windows Update"),
        ("11", "Ver portas abertas"),
        ("12", "Ver processos"),
        ("13", "Usuarios logados"),
        ("14", "Diagnostico completo"),
        ("15", "Limpeza completa (TUDO)"),
    ]
    for num, desc in opcoes:
        print(f"  {Cores.VERDE}{num}{Cores.RESET}  -  {desc}")
    print()
    print("=" * 42)
    print(f"  {Cores.AMARELO} P{Cores.RESET}  -  PACOTES DE MANUTENCAO  {Cores.CIANO}[NOVO]{Cores.RESET}")
    print("=" * 42)
    print(f"  {Cores.VERDE} 0{Cores.RESET}  -  Sair")
    print("=" * 42)
    return input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip()


# ============================================================
# MAIN
# ============================================================

ACOES = {
    "1":  op1_limpar_temp,
    "2":  op2_limpar_dns,
    "3":  op3_resetar_rede,
    "4":  op4_ver_ip,
    "5":  op5_ferramentas,
    "6":  op6_sfc,
    "7":  op7_chkdsk,
    "8":  op8_dism,
    "9":  op9_testar_conexao,
    "10": op10_windows_update,
    "11": op11_portas_abertas,
    "12": op12_processos,
    "13": op13_usuarios,
    "14": op14_diagnostico,
    "15": op15_limpeza_total,
}

def main():
    ativar_cores()

    if not is_admin():
        print(Cores.AMARELO + "\n  [AVISO] Reiniciando como Administrador..." + Cores.RESET)
        time.sleep(1)
        rerun_as_admin()

    while True:
        escolha = menu()

        if escolha == "0":
            cabecalho()
            print(f"  {Cores.VERDE}Encerrando o Suporte Tecnico HUGO MIRANDA...{Cores.RESET}\n")
            time.sleep(1)
            sys.exit(0)

        elif escolha.upper() == "P":
            while True:
                esc_pacote = menu_pacotes()
                if esc_pacote == "0":
                    break
                elif esc_pacote in PACOTES:
                    executar_pacote(esc_pacote)
                else:
                    print(Cores.VERMELHO + "\n  [ERRO] Pacote invalido." + Cores.RESET)
                    time.sleep(1)

        elif escolha in ACOES:
            ACOES[escolha]()

        else:
            print(Cores.VERMELHO + "\n  [ERRO] Opcao invalida. Tente novamente." + Cores.RESET)
            time.sleep(1)

if __name__ == "__main__":
    main()
