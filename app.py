import time
from Found import Found
from FoundClick import FoundClick
from FoundOneTime import FoundOneTime
from FoundClickOneTime import FoundClickOneTime
import subprocess
scriptSellRunes = "./Rune.py" 
if __name__ == "__main__":
    while True:
        RunEnded = Found("./img/button/RepetirBtn.png", threshold=0.8)
        if RunEnded == True:
            time.sleep(1)
            print(f"Executando Venda de Runas\n\n")
            subprocess.run(["python", scriptSellRunes])
            print(f"\n\nRunas Vendidas com Sucesso!\n")
            time.sleep(1)
            FoundClick("./img/button/RepetirBtn.png", threshold=0.8)
            time.sleep(1)
            FoundClick("./img/button/BatalhaDeRepeticao10Btn.png", threshold=0.8)