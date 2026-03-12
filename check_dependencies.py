import sys
import subprocess

required_packages = ['pandas', 'sklearn', 'numpy']

print("🔍 Vérification des dépendances...\n")

for package in required_packages:
    try:
        if package == 'sklearn':
            exec("import sklearn")
            print(f"✅ scikit-learn est installé")
        else:
            exec(f"import {package}")
            print(f"✅ {package} est installé")
    except ImportError:
        print(f"❌ {package} n'est PAS installé")
        print(f"   Installation avec: pip install {package}")

print("\n📁 Vérification du fichier CSV...")
import os
if os.path.exists("language.csv"):
    print("✅ language.csv trouvé")
else:
    print("❌ language.csv NON trouvé dans le dossier courant")
    print(f"   Dossier actuel: {os.getcwd()}")