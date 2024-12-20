import time
from Found import Found
from FoundClick import FoundClick
from FoundOneTime import FoundOneTime
from FoundClickOneTime import FoundClickOneTime

# Exemplo de uso
if __name__ == "__main__":
    while True:
        RunEnded = Found("./img/button/RepetirBtn.png", threshold=0.8)
        if RunEnded == True:
            time.sleep(2)
            FoundClick("./img/button/SelecionarTodosBtn.png", threshold=0.8)
            GetVenderItens = Found("./img/button/VenderBtn.png", threshold=0.8)
            if GetVenderItens == True:
                time.sleep(2)
                FoundClick("./img/button/VenderBtn.png", threshold=0.8)
                GetOk = FoundOneTime("./img/button/OkBtn.png", threshold=0.8)
                if GetOk == True:
                    time.sleep(2)
                    FoundClick("./img/button/OkBtn.png", threshold=0.8)
                    time.sleep(1)
                    FoundClick("./img/button/CancelarBtn.png", threshold=0.8)
                else:
                    time.sleep(2)
                    FoundClick("./img/button/SimBtn.png", threshold=0.8)
                    time.sleep(1)
                    RunaLegendPopup = FoundOneTime("./img/button/VenderRunaLegendBtn.png", threshold=0.8)
                    if RunaLegendPopup == True:
                        time.sleep(1)
                        FoundClick("./img/button/SimBtn.png", threshold=0.8)
                time.sleep(2)
                FoundClick("./img/button/RepetirBtn.png", threshold=0.8)
                time.sleep(2)
                FoundClickOneTime("./img/button/BatalhaDeRepeticao30Btn.png", threshold=0.8)

