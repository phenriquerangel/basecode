import os
import subprocess
import sys

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")
        return None

def get_pod():
    print("🔍 Procurando pod do backend...")
    pod = run_cmd("kubectl get pod -l app=backend -n estudos -o jsonpath='{.items[0].metadata.name}'")
    if not pod:
        print("❌ Backend não encontrado! O Kubernetes está rodando?")
        sys.exit(1)
    return pod

def backup():
    pod = get_pod()
    print(f"📦 Iniciando backup do pod: {pod}")
    run_cmd(f"kubectl exec {pod} -n estudos -- python manage.py dumpdata auth.User questions.Topico questions.Questao --indent 2 > backup_mathmaster.json")
    # Nota: Em alguns casos o nome da app é 'questoes', verifique se o dump fica vazio
    if os.path.exists("backup_mathmaster.json") and os.path.getsize("backup_mathmaster.json") < 10:
         # Tenta com o nome da app 'questoes'
         run_cmd(f"kubectl exec {pod} -n estudos -- python manage.py dumpdata auth.User questoes --indent 2 > backup_mathmaster.json")
    
    print(f"✅ Backup salvo em: {os.path.abspath('backup_mathmaster.json')}")

def restore():
    if not os.path.exists("backup_mathmaster.json"):
        print("❌ Arquivo 'backup_mathmaster.json' não encontrado na pasta atual.")
        return

    pod = get_pod()
    print(f"📥 Restaurando backup para o pod: {pod}")
    run_cmd(f"kubectl cp backup_mathmaster.json {pod}:/app/backup_restore.json -n estudos")
    run_cmd(f"kubectl exec -it {pod} -n estudos -- python manage.py loaddata backup_restore.json")
    print("✅ Dados restaurados com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python gerenciar_dados.py [backup|restore]")
    elif sys.argv[1] == "backup":
        backup()
    elif sys.argv[1] == "restore":
        restore()
    else:
        print("Comando inválido. Use 'backup' ou 'restore'.")