# Supreme-Bot
Supreme Bot è un sistema gratuito per Acquistare Articoli di Supreme nel Giorno del Drop del Negozio Supreme!

## Set Up
Scarica la cartella ZIP o clona il repository con:
```
git clone https://github.com/TonicStark/supreme-bot.git
```

Quindi installa le dipendenze in un virtualenv, puoi crearne uno tramite `python -m venv <name of the virtualenv>`, con:
```python
pip install -r requirements.txt
```

Dopo aver installato le dipendenze, esegui questo comando:
```
playwright install
```
Questo comando installerà tutti i Web Driver che ti serviranno per usare Playwright sulla tua macchina.

## Personalizzazione
Ora che hai impostato il tuo ambiente puoi aggiungere elementi al file `Items.json` con questa sequenza di parametri:

![code](../img/code.png)

Ora devi modificare i dati nel file `Data.json` in base alle tue esigenze, in questo modo:

![code](../img/code2.png)

## Avvia il bot
Ora devi solo eseguire il file `main.py` appena prima del rilascio, che è alle 12:00 in Italia. Puoi modificare le ore e i minuti nel file `bot.py`, in particolare:

![code](../img/code3.png)

Assicurati di includere gli articoli che desideri acquistare nell'elenco, che si trova nel file `Item.json` e sei a posto! Il Bot acquisterà gli articoli richiesti in pochi secondi! **Felice Shopping!**