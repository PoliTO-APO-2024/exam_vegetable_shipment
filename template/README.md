# Vegetable shipment
Adam Trask vuole trasportare verdure via treno attraverso gli USA, refrigerando i vagoni con del ghiaccio.
Ci sono varie città interessate all'acquisto, che offrono prezzi diversi.
Si chiede di scrivere un programma python che simuli le spedizioni.

I moduli e le classi vanno sviluppati nel package *shipment*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali ed esempi dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *ShipmentException* definito nel modulo *exceptions*.

## R1: Verdure e città (5/18)
La classe ```ShipmentManager``` nel modulo *shipment_manager* permette di definire le verdure trasportate e le città.

Il metodo
```add_vegetable(self, name: str, price_per_kg: float, heat_sensitivity: int, flavor_value: int) -> Vegetable```
permette di aggiungere una verdura, indicando il nome (che la identifica univocamente), il prezzo al kg, la sua sensibilità al caldo (da 1 a 10), e un valore legato al sapore (da 1 a 10).
Il metodo restituisce un oggetto della classe ```Vegetable```, definita nel modulo *elements*.
**ASSUMERE** e che i parametri forniti siano sempre corretti (**NON CONTROLLARE**).

La classe ```Vegetable``` ha le seguenti properties (in sola lettura):
- ```name(self) -> str```
- ```price_per_kg(self) -> float```
- ```heat_sensitivity(self) -> int```
- ```flavor_value(self) -> int```

che restituiscono gli attributi impostati tramite costruttore.

La rappresentazione degli oggetti ```Vegetable``` (```__repr__(self)```) deve essere una stringa composta dai valori delle diverse properties, nell'ordine in cui sono state elencate e separate da spazi.
Il prezzo al kg deve essere espresso su una sola cifra decimane, es:
*Carrot 0.9 6 9*

Il metodo ```add_city(self, name: str, value_fnc: Callable[[Vegetable, float], float]) -> None``` permette di aggiungere una città, lanciando un'eccezione se la città è già stata aggiunta.
Accetta come parametri il nome che la identifica univocamente e una funzione per la valutazione del prezzo delle verdure.

La funzione di valutazione accetta come parametri un oggetto ```Vegetable``` e di quanti gradi al di sopra della temperatura di conservazione la verdura è stata esposta, restituendo il prezzo al kg che la città offre per la verdura.

Il metodo ```get_cities(self) -> list[str]``` restituisce una lista contenente i nomi delle città che sono state aggiunte in **ORDINE ALFABETICO**.


## R2: Città e collegamenti (4/18)
La classe ```ShipmentManager``` permette di definire collegamenti ferroviari tra città e le verdure richieste da una città.

Il metodo ```add_connection(self, city_name_1: str, city_name_2: str, delta_t: float) -> None```
definisce un collegamento ferroviario ```UNIDIREZIONALE``` tra due città.
Il primo e il secondo parametro sono, rispettivamente, la città da cui parte il collegamento ferroviario e quella in cui arriva.
Il terzo parametro indica di quanti gradi la temperatura del prodotto trasportato cresce durante la tratta.

**NOTA BENE**: considerare che una città possa avere molteplici collegamenti in uscita, ma al più uno in entrata.
Questo fa si che le città siano sempre organizzate in una struttura ad albero tramite i suddetti collegamenti, partendo da una radice e arrivando alle foglie.

Il metodo ```get_connected(self, city_name: str) -> List[str]```, dato il nome di una città, restituisce l'elenco di nomi di città che sono raggiungibili partendo da essa e percorrendo un singolo collegamento ferroviario.
La lista di nomi restituita deve essere in **ORDINE CRESCENTE** secondo i gradi d'incremento della temperatura del prodotto durante la tratta.
Se nessuna città è raggiungibile restituire una lista vuota.

Il metodo ```add_city_request(self, city_name: str, *vegetables: Vegetable) -> int``` accetta come parametri il nome di una città e un numero variabile di oggetti ```Vegetable```, permettendo di specificare le verdure che sono richieste da una città.
Il metodo può essere invocato più volte sulla stessa città: se delle verdure erano state già richieste in passato non aggiungerle nuovamente.
Il metodo restituisce il numero di verdure effettivamente aggiunto.

## R3: Vagoni (3/18)
La classe ```ShipmentManager``` permette di definire il contenuto dei vagoni per il trasporto di verdure, e d'individuare le città interessate a ciascuno.

Il metodo
```add_train_car(self, car_id: int, weight: int, *vegetables: Vegetable) -> None```
permette di aggiungere un nuovo vagone.
Accetta come parametri l'identificativo numerico che identifica univocamente il vagone, il peso del carico che può trasportare, e un numero variabile di oggetti ```Vegetable``` trasportati.

Il metodo
```get_train_cars_for_cities(self) -> dict[str, List[int]]```
restituisce un dizionario che ha per chiavi i nomi delle città, e per valori delle liste con i codici dei vagoni ammissibili per la città **ORDINATI** in senso crescente.
Un vagone è ammissibile per una città se almeno uno dei prodotti contenuti è richiesto dalla città.
Se una città non ha vagoni ammissibili (o non richiede prodotti) non deve essere inserita nel dizionario.

## R4: Temperatura (3/18)
La classe ```ShipmentManager``` permette di analizzare il percorso tra due città.

Il metodo
```get_temp_increment(self, city_start_name: str, city_end_name: str) -> Optional[float]```
accetta come parametri una città di partenza e una città di arrivo.
Esso restituisce di quanti gradi aumenta la temperatura del prodotto durante l'intero percorso.
L'aumento complessivo è data dalla somma delle singole tratte.
Se non esiste un percorso tra le due città, restituire ```None```.

**IMPORTANTE**: ricordare che i collegamenti sono unidirezionali, non è quindi possibile avere tratte che "risalgono" l'albero.


## R5 Valutazione (3/18)
La classe ```ShipmentManager``` permette di stabilire il valore del carico di un vagone per una città e trovare la città che fornisce il guadagno maggiore.

Il metodo
```get_train_car_value(self, car_id, city_name, start_city = None)```
permette di ottenere il valore del carico di un vagone per una città.
Accetta come parametri l'identificativo di un vagone, il nome della città a cui vendere il carico e un parametro opzionale che indica la città da cui il vagone parte.

Trovare il prezzo al kg per ogni verdura trasportata utilizzando la funzione di valutazione specifica per la città di vendita.
Dopodiché calcolare il prezzo totale in base peso del carico trasportato dal vagone.
Considerare che le diverse verdure sono presenti nel vagone nelle stesse quantità.
Se viene fornita una città di partenza, calcore l'aumento in gradi della temperatura del carico durante il percorso e fornirlo alla funzione di valutazione.
Se non è indicata, invece, fornire zero.

**IMPORTANTE**: valutare **TUTTE** le verdure trasportate dal vagone, non solo quelle richieste dalla città.


Il metodo
```get_best_deal(self, car_id)```
accetta come parametro l'identificativo di un vagone e restituisce il prezzo massimo offerto dalle città per il carico.
Usare la il metodo definito precedentemente per valutare il prezzo per ciascuna città, lasciando la città di partenza non specificata.
