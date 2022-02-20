# Supreme-Bot
Questo è il mio Bot Supreme personale, per l'acquisto di oggetti nel giorno del Drop di Supreme!

## Set Up
Scarica la cartella ZIP o clona il repository con:
```
git clone https://github.com/TonicStark/Supreme-Bot.git
```

Quindi installa le dipendenze in un virtualenv, puoi crearne uno tramite `python -m venv <name of the virtualenv>`, con:
```python
pip install -r requirements.txt
```

Dopo ave rinstallato le dipendenze, esegui questo comando:
```
playwright install
```
Questo comando installerà tutti i Web Driver che ti serviranno per usare Playwright sulla tua macchina.

## Personalizzazione
Ora che hai impostato il tuo ambiente puoi aggiungere elementi al file `Items.json` con questa sequenza di parametri:

```JSON
[
    {
        "Articolo": "Nome dell'articolo",
        "Stile": "Colore",
        "Taglia": "Taglia",
        "Tipo": "Categoria"
    }
]
```

Ora devi modificare i dati nel file `Data.json` in base alle tue esigenze, in questo modo:

```JSON
[
    {
        "Nome Cognome": "Il tuo nome e cognome",
        "E-mail": "La tua e-mail",
        "Tel": "Il tuo numero di telefono",
        "Indirizzo": "Il tuo indirizzo",
        "N": "Il tuo numero civico",
        "Città": "La tua città",
        "Codice postale": "Il tuo codice postale",
        "Numero di carta": "Numero di carta di credito",
        "CVV": "Token di verifica della tua carta"
    }
]
```

## Avvia il bot
Ora devi solo eseguire il file `main.py` appena prima del rilascio, che è alle 12:00 in Italia. Puoi modificare le ore e i minuti nel file `bot.py`, in particolare:
```python
# Orari
self.HOUR = "12"
self.MINUTE = "00"
```
Assicurati di includere gli articoli che desideri acquistare nell'elenco, che si trova nel file `Item.json` e sei a posto! Il Bot acquisterà gli articoli richiesti in pochi secondi! **Felice Shopping!**