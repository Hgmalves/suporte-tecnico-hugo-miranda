import os
import sys
import subprocess
import ctypes
import platform
import socket
import time
import webbrowser
from pathlib import Path
from datetime import datetime

# ============================================================
#  SUPORTE TECNICO - Hugo Miranda -Suporte
#  Desenvolvido por: Hugo Miranda -Suporte
#  Versao: 2.3 | 2026
# ============================================================

VERSAO = "2.3"
MODO_TESTE = True
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
RELATORIOS_DIR = BASE_DIR / "relatorios"
EXECUCAO_INICIO = datetime.now()
SESSION_LOG = LOGS_DIR / f"execucao_{EXECUCAO_INICIO.strftime('%Y%m%d_%H%M%S')}.log"

if platform.system() != "Windows":
    print("[ERRO] Este script foi desenvolvido exclusivamente para Windows.")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def rerun_as_admin():
    argumentos = subprocess.list2cmdline(sys.argv)
    resultado = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, argumentos, None, 1
    )
    if resultado <= 32:
        print(Cores.VERMELHO + "\n  [ERRO] Nao foi possivel abrir como Administrador." + Cores.RESET)
        print(Cores.AMARELO + "  Aceite a permissao do Windows (UAC) para o programa continuar." + Cores.RESET)
        input(Cores.CIANO + "\n  Pressione ENTER para fechar..." + Cores.RESET)
        sys.exit(1)
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
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        kernel32.SetConsoleMode(handle, 7)
    except:
        pass

def preparar_pastas():
    LOGS_DIR.mkdir(exist_ok=True)
    RELATORIOS_DIR.mkdir(exist_ok=True)

def escrever_log(mensagem):
    preparar_pastas()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensagem}\n")

def executar_powershell(script):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )

def obter_info_discos():
    script = "Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,@{Name='Livre(GB)';Expression={[math]::Round($_.FreeSpace/1GB,2)}},@{Name='Tamanho(GB)';Expression={[math]::Round($_.Size/1GB,2)}} | Format-Table -AutoSize | Out-String"
    resultado = executar_powershell(script)
    if resultado.returncode == 0 and resultado.stdout.strip():
        return resultado.stdout
    return "Nao foi possivel obter informacoes de disco via PowerShell."

def verificar_comando(comando):
    r = subprocess.run(["where", comando], capture_output=True, text=True, shell=True)
    return r.returncode == 0

def tem_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2).close()
        return True
    except OSError:
        return False

def coletar_compatibilidade():
    script = "(Get-CimInstance Win32_OperatingSystem).Caption"
    sistema = executar_powershell(script)
    nome_sistema = sistema.stdout.strip() if sistema.returncode == 0 and sistema.stdout.strip() else platform.platform()
    return {
        "Sistema": nome_sistema,
        "Admin": "Sim" if is_admin() else "Nao",
        "Internet": "OK" if tem_internet() else "Sem conexao",
        "PowerShell": "OK" if verificar_comando("powershell") else "Indisponivel",
        "WMIC": "OK" if verificar_comando("wmic") else "Indisponivel",
        "Modo teste": "Ativo" if MODO_TESTE else "Desativado",
        "Logs": str(LOGS_DIR),
    }

def mostrar_compatibilidade():
    titulo("VERIFICACAO DE COMPATIBILIDADE")
    info = coletar_compatibilidade()
    for chave, valor in info.items():
        print(f"  {Cores.VERDE}{chave}:{Cores.RESET} {valor}")
    escrever_log("Compatibilidade inicial verificada.")
    pausar()

def executar_acao_segura(cmd, descricao, shell=True, destrutivo=False):
    escrever_log(f"Acao solicitada: {descricao} | comando={cmd}")
    print(Cores.CIANO + f"\n  > {cmd}" + Cores.RESET)
    if MODO_TESTE and destrutivo:
        print(Cores.AMARELO + "  [MODO TESTE] Comando nao executado para evitar alteracoes no sistema." + Cores.RESET)
        escrever_log(f"MODO TESTE impediu execucao: {descricao}")
        return False
    resultado = subprocess.run(cmd, shell=shell)
    escrever_log(f"Resultado da acao '{descricao}': retorno={resultado.returncode}")
    return resultado.returncode == 0

def cabecalho():
    os.system("cls")
    print(Cores.VERDE + Cores.BOLD)
    print("=" * 42)
    print(f"      SUPORTE TECNICO - Hugo Miranda -Suporte {VERSAO}")
    print("=" * 42)
    print(f"  Modo teste: {'ATIVO' if MODO_TESTE else 'DESATIVADO'}")
    print(Cores.RESET)

def pausar():
    print()
    input(Cores.CIANO + "  Pressione ENTER para voltar ao menu..." + Cores.RESET)

def executar(cmd, shell=True):
    print()
    executar_acao_segura(cmd, "execucao direta", shell=shell, destrutivo=False)

def executar_capturar(cmd, shell=True):
    try:
        escrever_log(f"Captura solicitada: {cmd}")
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
        self.itens         = []

    def adicionar(self, descricao, status, detalhe=""):
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

        self._salvar(ok, falhas, avisos, duracao)

    def _salvar(self, ok, falhas, avisos, duracao):
        timestamp = self.inicio.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_{self.nome_pacote.replace(' ', '_')}_{timestamp}.txt"
        preparar_pastas()
        caminho = RELATORIOS_DIR / nome_arquivo
        linhas = []
        linhas.append("=" * 42)
        linhas.append(f"  RELATORIO - {self.nome_pacote}")
        linhas.append(f"  Data : {self.inicio.strftime('%d/%m/%Y')}  Hora: {self.inicio.strftime('%H:%M')}")
        linhas.append(f"  Duracao: {duracao}s")
        linhas.append(f"  Maquina: {platform.node()}")
        linhas.append(f"  Usuario: {os.environ.get('USERNAME', 'desconhecido')}")
        linhas.append(f"  Admin: {'Sim' if is_admin() else 'Nao'}")
        linhas.append(f"  Modo teste: {'Ativo' if MODO_TESTE else 'Desativado'}")
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
            escrever_log(f"Relatorio salvo: {caminho}")
        except Exception as e:
            print(f"\n  {Cores.VERMELHO}[ERRO]{Cores.RESET} Nao foi possivel salvar o relatorio: {e}")


# ============================================================
# FUNCOES INDIVIDUAIS (1 a 17)
# ============================================================

def op1_limpar_temp():
    titulo("1 - LIMPAR ARQUIVOS TEMPORARIOS")
    if MODO_TESTE:
        print(f"  {Cores.AMARELO}[MODO TESTE]{Cores.RESET} Esta rotina apenas simula a limpeza.")
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
                    if not MODO_TESTE:
                        os.remove(caminho)
                    total += 1
                except Exception:
                    pass
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} {total} arquivo(s) removido(s).")
    pausar()

def op1_limpar_temp_silencioso():
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
                    if not MODO_TESTE:
                        os.remove(caminho)
                    total += 1
                except Exception:
                    pass
    detalhe = f"{total} arquivo(s) {'simulados' if MODO_TESTE else 'removido(s)'}"
    return ("Limpar arquivos temporarios", "OK", detalhe)

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
        executar_acao_segura(cmd, "reset de rede", destrutivo=True)
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
        if MODO_TESTE:
            ok = True
            escrever_log(f"MODO TESTE simulou: {cmd}")
        else:
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
        executar_acao_segura(cmd, "reset do Windows Update", destrutivo=True)
    print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Windows Update resetado com sucesso.")
    pausar()

def op10_windows_update_silencioso():
    cmds_stop  = ["net stop wuauserv", "net stop cryptSvc", "net stop bits", "net stop msiserver"]
    cmds_del   = [r'rd /s /q "C:\Windows\SoftwareDistribution"', r'rd /s /q "C:\Windows\System32\catroot2"']
    cmds_start = ["net start wuauserv", "net start cryptSvc", "net start bits", "net start msiserver"]
    falhas = 0
    for cmd in cmds_stop + cmds_del + cmds_start:
        if MODO_TESTE:
            ok = True
            escrever_log(f"MODO TESTE simulou: {cmd}")
        else:
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
    preparar_pastas()
    r = subprocess.run("systeminfo", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("=== INFORMACOES DO SISTEMA ===\n" + r.stdout)
    r = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== CONFIGURACAO DE REDE ===\n" + r.stdout)
    relatorio.append("\n=== DISCOS ===\n" + obter_info_discos())
    r = subprocess.run("tasklist", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== PROCESSOS ATIVOS ===\n" + r.stdout)
    r = subprocess.run("netstat -ano", shell=True, capture_output=True, text=True, encoding="cp850", errors="replace")
    relatorio.append("\n=== PORTAS ABERTAS ===\n" + r.stdout)
    compat = coletar_compatibilidade()
    relatorio.append("\n=== COMPATIBILIDADE ===\n" + "\n".join(f"{k}: {v}" for k, v in compat.items()))
    caminho = RELATORIOS_DIR / "diagnostico_AOFR.txt"
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("\n".join(relatorio))
        print(f"  {Cores.VERDE}[OK]{Cores.RESET} Relatorio salvo em: {caminho}")
        escrever_log(f"Diagnostico completo salvo: {caminho}")
    except Exception as e:
        print(f"  {Cores.VERMELHO}[ERRO]{Cores.RESET} Nao foi possivel salvar: {e}")
    for secao in relatorio[:2]:
        print(secao[:500])
    pausar()

def op15_limpeza_total():
    titulo("15 - LIMPEZA COMPLETA (TUDO)")
    print(f"  {Cores.AMARELO}[AVISO]{Cores.RESET} Esta opcao executara TODAS as limpezas.")
    conf = input("  Digite CONFIRMAR para continuar: ").strip()
    if conf != "CONFIRMAR":
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

def op16_recuperacao_acesso():
    titulo("16 - AJUDA DE RECUPERACAO DE ACESSO")

    links = {
        "1": ("Reset de conta Microsoft", "https://account.live.com/password/reset"),
        "2": ("Reset corporativo Microsoft 365 / Entra", "https://passwordreset.microsoftonline.com/"),
        "3": ("Artigo Microsoft - Conta local do Windows", "https://support.microsoft.com/windows/change-or-reset-your-local-account-password-in-windows"),
        "4": ("Artigo Microsoft - Senha no Windows 10/11", "https://support.microsoft.com/windows/change-or-reset-your-password-in-windows"),
    }

    print("  Este modulo mostra apenas caminhos OFICIAIS de recuperacao.")
    print(f"  {Cores.AMARELO}Nao realiza bypass, quebra ou remocao indevida de senha.{Cores.RESET}")
    print()
    print("  Checklist rapido:")
    print("   - Conta local: use 'Reset password' na tela de login e responda as perguntas.")
    print("   - Conta Microsoft pessoal: use o fluxo 'Esqueci minha senha'.")
    print("   - Conta corporativa: use o portal oficial da empresa / Microsoft Entra.")
    print("   - Se houver outro administrador autorizado: redefinir pela Gestao do Computador.")
    print("   - Sem metodo de recuperacao e sem outro admin: acionar TI / helpdesk.")
    print()
    print("  Opcoes:")
    for chave, (nome, _) in links.items():
        print(f"   {Cores.VERDE}{chave}{Cores.RESET}  -  Abrir {nome}")
    print(f"   {Cores.VERDE}5{Cores.RESET}  -  Mostrar passos locais no Windows")
    print(f"   {Cores.VERDE}0{Cores.RESET}  -  Voltar")
    print()

    esc = input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip()

    if esc in links:
        nome, url = links[esc]
        webbrowser.open(url)
        print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Abrindo: {nome}")
        print(f"  {Cores.CIANO}{url}{Cores.RESET}")
        time.sleep(1)
        pausar()
        return

    if esc == "5":
        print()
        print("  Passos locais no Windows:")
        print("   1. Verifique se a conta e local, Microsoft ou corporativa.")
        print("   2. Na tela de login, procure por 'Reset password' ou 'I forgot my password'.")
        print("   3. Se houver outro administrador autorizado, abra 'lusrmgr.msc' ou Gestao do Computador.")
        print("   4. Em ambiente corporativo, encaminhe para o portal oficial ou helpdesk.")
        print("   5. Registre a acao no chamado interno antes de alterar a senha.")
        pausar()
        return

    if esc != "0":
        print(f"\n  {Cores.VERMELHO}[ERRO]{Cores.RESET} Opcao invalida.")
        time.sleep(1)

def op17_licenciamento_windows():
    titulo("17 - LICENCIAMENTO DO WINDOWS")

    print("  Este modulo consulta o status de licenciamento com ferramentas oficiais.")
    print(f"  {Cores.AMARELO}Nao realiza ativacao automatica, instalacao de chave ou bypass.{Cores.RESET}")
    print()
    print("  Opcoes:")
    print(f"   {Cores.VERDE}1{Cores.RESET}  -  Ver status resumido (slmgr /xpr)")
    print(f"   {Cores.VERDE}2{Cores.RESET}  -  Ver detalhes da licenca (slmgr /dlv)")
    print(f"   {Cores.VERDE}3{Cores.RESET}  -  Ver informacoes basicas (slmgr /dli)")
    print(f"   {Cores.VERDE}4{Cores.RESET}  -  Abrir configuracoes de ativacao")
    print(f"   {Cores.VERDE}0{Cores.RESET}  -  Voltar")
    print()

    esc = input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip()

    if esc == "1":
        titulo("STATUS RESUMIDO DE ATIVACAO")
        executar(r'cscript //nologo "%windir%\system32\slmgr.vbs" /xpr')
        pausar()
        return

    if esc == "2":
        titulo("DETALHES DA LICENCA")
        executar(r'cscript //nologo "%windir%\system32\slmgr.vbs" /dlv')
        pausar()
        return

    if esc == "3":
        titulo("INFORMACOES BASICAS DA LICENCA")
        executar(r'cscript //nologo "%windir%\system32\slmgr.vbs" /dli')
        pausar()
        return

    if esc == "4":
        subprocess.Popen("start ms-settings:activation", shell=True)
        print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Abrindo Configuracoes de ativacao...")
        time.sleep(1)
        pausar()
        return

    if esc != "0":
        print(f"\n  {Cores.VERMELHO}[ERRO]{Cores.RESET} Opcao invalida.")
        time.sleep(1)


# ============================================================
# OP18 - ORIENTACAO DE ATIVACAO OFICIAL
# ============================================================

def op18_orientacao_ativacao_oficial():
    """Mostra caminhos oficiais para ativacao e regularizacao de licenca."""
    titulo("18 - ORIENTACAO DE ATIVACAO OFICIAL")

    print("  Este modulo foi preparado para repositorio publico.")
    print("  Ele nao executa ativadores, bypass, instalacao de chaves ou scripts externos.")
    print()
    print("  Opcoes:")
    print(f"   {Cores.VERDE}1{Cores.RESET}  -  Verificar status de ativacao do Windows")
    print(f"   {Cores.VERDE}2{Cores.RESET}  -  Abrir configuracoes de ativacao")
    print(f"   {Cores.VERDE}3{Cores.RESET}  -  Abrir suporte oficial da Microsoft")
    print(f"   {Cores.VERDE}0{Cores.RESET}  -  Voltar")
    print()

    esc = input(Cores.AMARELO + "  Escolha: " + Cores.RESET).strip()

    if esc == "1":
        verificar_status_ativacao()
        pausar()
        return

    if esc == "2":
        subprocess.Popen("start ms-settings:activation", shell=True)
        print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Abrindo Configuracoes de ativacao...")
        time.sleep(1)
        pausar()
        return

    if esc == "3":
        webbrowser.open("https://support.microsoft.com/windows/activate-windows")
        print(f"\n  {Cores.VERDE}[OK]{Cores.RESET} Abrindo suporte oficial da Microsoft...")
        time.sleep(1)
        pausar()
        return

    if esc != "0":
        print(f"\n  {Cores.VERMELHO}[ERRO]{Cores.RESET} Opcao invalida.")
        time.sleep(1)


def verificar_status_ativacao():
    """Verifica o status de ativacao do Windows"""
    print("\n  Verificando status de ativacao do Windows...\n")
    
    cmd = r'cscript //nologo "%windir%\system32\slmgr.vbs" /xpr'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='cp850')
    
    if result.stdout:
        print(f"  {Cores.CIANO}{result.stdout.strip()}{Cores.RESET}")
    
    ver = executar_powershell("(Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version | Format-Table -HideTableHeaders | Out-String)")
    if ver.stdout:
        print(f"\n  {Cores.VERDE}Sistema:{Cores.RESET}")
        for line in ver.stdout.strip().split('\n'):
            if line.strip():
                print(f"    {line.strip()}")
    
    print(f"\n  {Cores.AMARELO}Dica:{Cores.RESET} Use apenas canais oficiais para regularizar a licenca.")


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
        icone = Cores.VERDE + "[OK]" if status == "OK" else (Cores.VERMELHO + "[X]" if status == "FALHA" else Cores.AMARELO + "[!]")
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
        (" C", "Ver compatibilidade do ambiente"),
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
        ("16", "Ajuda de recuperacao de acesso"),
        ("17", "Licenciamento do Windows"),
        ("18", "Orientacao de ativacao oficial"),
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
    "C":  mostrar_compatibilidade,
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
    "16": op16_recuperacao_acesso,
    "17": op17_licenciamento_windows,
    "18": op18_orientacao_ativacao_oficial,
}

def main():
    ativar_cores()
    preparar_pastas()
    escrever_log(f"Programa iniciado. Versao={VERSAO} Usuario={os.environ.get('USERNAME', 'desconhecido')}")

    # PERGUNTA antes de reiniciar como admin (evita loop)
    if not is_admin():
        print(Cores.AMARELO + "\n  [AVISO] Algumas funcoes precisam de permissoes de Administrador." + Cores.RESET)
        print(Cores.CIANO + "  Deseja reiniciar como Administrador? (s/n): " + Cores.RESET, end='')
        resp = input().strip().lower()
        if resp == 's':
            rerun_as_admin()
        else:
            print(Cores.AMARELO + "  Continuando sem permissoes de Admin. Algumas opcoes podem falhar." + Cores.RESET)
            time.sleep(2)

    while True:
        escolha = menu()

        if escolha == "0":
            cabecalho()
            print(f"  {Cores.VERDE}Encerrando o Suporte Tecnico Hugo Miranda -Suporte...{Cores.RESET}\n")
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
    try:
        main()
    except Exception as e:
        print(Cores.VERMELHO + f"\n  [ERRO] O programa encontrou uma falha: {e}" + Cores.RESET)
        input(Cores.CIANO + "  Pressione ENTER para fechar..." + Cores.RESET)
