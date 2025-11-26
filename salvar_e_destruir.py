import os
import subprocess
import time

def run_command(command, ignore_errors=False):
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            print(f"❌ Erro ao executar: {command}")
            print(e.output)
        return None

print("🚨 INICIANDO PROTOCOLO DE DESTRUIÇÃO COM BACKUP 🚨")

# 1. Identificar o Pod do Backend
print("\n🔍 Procurando backend para backup...")
pod_name = run_command("kubectl get pod -l app=backend -n estudos -o jsonpath='{.items[0].metadata.name}'", ignore_errors=True)

if pod_name:
    print(f"✅ Pod encontrado: {pod_name}")
    print("📦 Extraindo dados (Questões, Tópicos, Usuários)...")
    
    # Faz o dump de tudo (auth para usuários, questoes para o conteúdo)
    # Excluímos contenttypes e sessions para evitar conflitos na volta
    cmd_dump = (
        f"kubectl exec -it {pod_name} -n estudos -- "
        f"python manage.py dumpdata auth questoes --indent 2 "
        f"> backup_full.json"
    )
    run_command(cmd_dump)
    
    if os.path.exists("backup_full.json") and os.path.getsize("backup_full.json") > 10:
        print(f"💾 BACKUP SALVO COM SUCESSO: {os.path.abspath('backup_full.json')}")
    else:
        print("⚠️ AVISO: O arquivo de backup parece vazio ou falhou.")
        confirm = input("Deseja continuar a destruição SEM backup? (s/n): ")
        if confirm.lower() != 's':
            exit()
else:
    print("⚠️ Backend não encontrado. Impossível fazer backup.")
    confirm = input("Deseja destruir a infraestrutura mesmo assim? (s/n): ")
    if confirm.lower() != 's':
        exit()

# 2. Destruir Kubernetes
print("\n🔥 Destruindo Namespace 'estudos' (Isso apaga Pods, Services e Volumes)...")
run_command("kubectl delete namespace estudos", ignore_errors=True)

# 3. Limpar Arquivos Locais
print("\n🗑️ Removendo pasta de código 'basecode'...")
# No Windows usa rmdir, no Linux/Mac rm -rf
if os.name == 'nt':
    os.system('rmdir /S /Q basecode')
else:
    os.system('rm -rf basecode')

print("\n💀 DESTRUIÇÃO CONCLUÍDA.")
print("Os seus dados estão salvos em 'backup_full.json'.")
print("Para reconstruir, use o script 'reconstruir_tudo.py'.")