# Abitur 2015 Mathematik Stochastik IV

## Aufgabe A 1
In einer Urne befinden sich vier rote und sechs blaue Kugeln. Aus dieser wird achtmal eine Kugel zufällig gezogen, die Farbe notiert und die Kugel anschließend wieder zurückgelegt.

### Teilaufgabe Teil A 1a (2 BE)

In einer Urne befinden sich vier rote und sechs blaue Kugeln. Aus dieser wird achtmal eine Kugel zufällig gezogen, die Farbe notiert und die Kugel anschließend wieder zurückgelegt.

Geben Sie einen Term an, mit dem die Wahrscheinlichkeit des Ereignisses „Es werden gleich viele rote und blaue Kugeln gezogen." berechnet werden kann.

### Lösung zu Teilaufgabe Teil A 1a

_**Binomialverteilung**_

$A$ : „Es werden gleich viele rote und blaue Kugeln gezogen.“

4 rote Kugeln +6 blaue Kugeln $=10$ Kugeln

$p=P($,rote Kugel“ $)=\frac{4}{10}=\frac{2}{5}$

$q=1-p=\frac{3}{5}$

$P(A)=P_{\frac{2}{5}}^{8}(X=4)$

$$
P(A)=\left(\begin{array}{l}
8 \\
4
\end{array}\right) \cdot\left(\frac{2}{5}\right)^{4} \cdot\left(\frac{3}{5}\right)^{4}
$$

#### Erläuterung: Bernoulli-Kette

Das Zufallsexperiment kann als Bernoulli-Kette der Länge $n=8$ mit der Trefferwahrscheinlichkeit $p=\frac{2}{5}$ angesehen werden.

$n=8$

$k=4$


#### Erläuterung: Bernoulli-Formel

Die Wahrscheinlichkeit genau $k$ Treffer bei $n$ Versuchen zu erzielen beträgt:

$P(\mathrm{k}$ Treffer $)=P_{p}^{n}(X=k)=\left(\begin{array}{l}n \\ k\end{array}\right) \cdot p^{k} \cdot(1-p)^{n-k}$

Dabei ist:

$n=$ Anzahl der Versuch

$k=$ Anzahl der Treffer

$p=$ Wahrscheinlichkeit eines Treffers pro Versuch

$1-p=$ Wahrscheinlichkeit einer Niete pro Versuch


### Teilaufgabe Teil A 1b (3 BE)

Beschreiben Sie im Sachzusammenhang jeweils ein Ereignis, dessen Wahrscheinlichkeit durch den angegebenen Term berechnet werden kann.
a) $1-\left(\frac{3}{5}\right)^{8}$

в) $\left(\frac{3}{5}\right)^{8}+8 \cdot \frac{2}{5} \cdot\left(\frac{3}{5}\right)^{7}$

### Lösung zu Teilaufgabe Teil A 1b

**_Binomialverteilung_**

a) $1-\left(\frac{3}{5}\right)^{8}$

z. B.: Es wird mindestens eine rote Kugel gezogen.

в) $\left(\frac{3}{5}\right)^{8}+8 \cdot \frac{2}{5}\left(\frac{3}{5}\right)^{7}$

z. B.: Es werden mindestens 7 blaue Kugeln gezogen.

#### Erläuterung: Bernoulli-Formel

Term untersuchen:

$\frac{3}{5}$ ist die Wahrscheinlichkeit eine blaue Kugel zu ziehen.

$\left(\frac{3}{5}\right)^{8}$ ist die Wahrscheinlichkeit nur blaue Kugeln zu ziehen. Anders ausgedrückt: die Wahrscheinlichkeit keine rote Kugel zu ziehen.

$1-P$ (Ereignis) stellt die Wahrscheinlichkeit des Gegenereignisses dar. Das Gegenereignis zu „keine rote Kugel“ lautet „mindestens eine rote Kugel“.

Als Ergebnis der Bernoulli-Formel mit $n=8, k \geq 1$ und $p=\frac{2}{5}$ (= Wahrscheinlichkeit für eine rote Kugel):

$$
P_{\frac{2}{5}}^{8}(X \geq 1)=1-P_{\frac{2}{5}}^{8}(X=0)=1-\underbrace{\left(\begin{array}{l}
8 \\
0
\end{array}\right) \cdot\left(\frac{2}{5}\right)^{0}} \cdot\left(\frac{3}{5}\right)^{8}=1-\left(\frac{3}{5}\right)^{8}
$$

#### Erläuterung: Bernoulli-Forme

Term untersuchen:

$\left(\frac{3}{5}\right)^{8}$ ist die Wahrscheinlichkeit 8 blaue Kugeln zu ziehen.

$8 \cdot \frac{2}{5}\left(\frac{3}{5}\right)^{7}$ kann geschrieben werden als $\left(\begin{array}{l}8 \\ 1\end{array}\right) \cdot\left(\frac{2}{5}\right)^{1}\left(\frac{3}{5}\right)^{7}$. Dieser Term entspricht der Bernoulli-Formel für $n=8, k=1$ und $p=\frac{2}{5}$ (rote Kugel), also $P_{\frac{2}{2}}^{8}(X=1)$. Das ist die Wahrscheinlichkeit eine rote Kugel zu ziehen, oder anders ausgedrückt, die Wahrscheinlichkeit 7 blaue Kugeln zu ziehen.

Die Summe der beiden Terme bedeutet, dass Alternativen zusammenaddier werden.

$\left(\frac{3}{5}\right)^{8}+8 \cdot \frac{2}{5}\left(\frac{3}{5}\right)^{7}$ ist also die Wahrscheinlichkeit entweder 8 blaue Kugeln oder 7 blaue Kugeln zu ziehen. Dies kann mit „mindestens 7 blaue Kugeln ausgedrückt werden.


## Aufgabe A 2

Für ein Zufallsexperiment wird eine Zufallsgröße $X$ festgelegt, welche die drei Werte $-2,1$ und 2 annehmen kann. In der Abbildung ist die Wahrscheinlichkeitsverteilung von $X$ dargestellt.

```python
import matplotlib.pyplot as plt

# Data for plotting
values = [-2, 1, 2]
probabilities = [0.25, 0.25, 0.5]

# Create the bar plot
plt.bar(values, probabilities, color='blue')

# Labeling the axes
plt.xlabel('k')
plt.ylabel('P(X=k)')

# Setting the title
plt.title('Probability Distribution')

# Displaying the plot
plt.show()
```

### Teilaufgabe Teil A 2a (2 BE)

Ermitteln Sie mithilfe der Abbildung den Erwartungswert der Zufallsgröße $X$.

### Lösung zu Teilaufgabe Teil A 2a

_**Erwartungswert einer Zufallsgröße**_

Wahrscheinlichkeitsverteilung als Tabelle:

$$
\begin{array}{c|c|c|c}
k_{i} & -2 & 1 & 2 \\
\hline P\left(X=k_{i}\right) & 0,25 & 0,25 & 0,5
\end{array}
$$

$$
E_{n}(X)=\sum_{i=1}^{n} x_{i} \cdot P\left(X=x_{i}\right)
$$[^0]

#### Erläuterung: Erwartungswert einer Zufallsgröß

Der Erwartungswert einer Zufallsgröße $X$ bei $n$ Versuchen (hier 3), ist definiert als:


### Teilaufgabe Teil A 2 b (3 BE)

Das Zufallsexperiment wird zweimal durchgeführt. Dabei wird jeweils der Wert der Zufallsgröße $X$ notiert. Bestimmen Sie die Wahrscheinlichkeit dafür, dass die Summe dieser beiden Werte negativ ist.

### Lösung zu Teilaufgabe Teil A 2b

_**Wahrscheinlichkeit**_

Baumdiagramm erstellen:

```python
from graphviz import Digraph

# Initialize Digraph object
dot = Digraph()

# Adding nodes and edges with labels for probabilities
dot.node('A', '-2')
dot.node('B', '1')
dot.node('C', '2')

# Edges for left side of the tree
dot.edges([('A', 'B'), ('B', 'A')])
dot.edge('A', 'B', '0.25', constraint='false')
dot.edge('B', 'A', '0.25', constraint='false')

# Edges for right side of the tree
dot.edge('C', 'A', '0.5', constraint='false')
dot.edge('C', 'B', '0.25', constraint='false')
dot.edge('B', 'C', '0.25', constraint='false')

# Display the graph
dot.view()
```

$P($,.Summe ist negativ" $)=\frac{1}{4} \cdot \frac{1}{4}+\frac{1}{4} \cdot \frac{1}{4}+\frac{1}{4} \cdot \frac{1}{4}=\frac{3}{16}$

#### Erläuterung: Wahrscheinlichkeit

Die Wahrscheinlichkeiten werden der Wahrscheinlichkeitsverteilung aus Teil A Teilaufgabe 2a entnommen.

#### Erläuterung: 1. Pfadregel, 2. Pfadregel

1. Pfadregel: In einem Baumdiagramm ist die Wahrscheinlichkeit eines Ereignisses gleich dem Produkt der Wahrscheinlichkeiten längs des zugehörigen Pfades.

In diesem Fall:

$P(-2 \cap-2)=P(-2) \cdot P_{-2}(-2)=\frac{1}{4} \cdot \frac{1}{4}$

$P(-2 \cap 1)=P(-2) \cdot P_{-2}(1)=\frac{1}{4} \cdot \frac{1}{4}$

$P(1 \cap-2)=P(1) \cdot P_{1}(-2)=\frac{1}{4} \cdot \frac{1}{4}$

2. Pfadregel: In einem Baumdiagramm ist die Wahrscheinlichkeit eines Ereignisse gleich der Summe der für dieses Ereignis zugehörigen Pfadwahrscheinlichkeiten.

In diesem Fall: $\quad P(.$, Summe ist negativ“ $)=P(-2 \cap-2)+P(-2 \cap 1)+P(1 \cap-2)$


## Aufgabe B 1
Die beiden Diagramme zeigen für die Bevölkerungsgruppe der über 14-Jährigen in Deutschland Daten zur Altersstruktur und zum Besitz von Mobiltelefonen.

```python
import matplotlib.pyplot as plt

# Data for the pie charts
age_groups_1 = [73, 24, 3]  # Percentages for the first pie chart
age_groups_2 = [90, 10]     # Percentages for the second pie chart

labels_1 = ['15 bis 17 Jahre alt', '18 bis 64 Jahre alt', '65 Jahre und älter']
labels_2 = ['besitzen kein Mobiltelefon', 'besitzen ein Mobiltelefon']

# Create figure and axes
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# First pie chart
axs[0].pie(age_groups_1, labels=labels_1, autopct='%1.0f%%', startangle=90)
axs[0].set_title('Age Distribution 1')

# Second pie chart
axs[1].pie(age_groups_2, labels=labels_2, autopct='%1.0f%%', startangle=90)
axs[1].set_title('Age Distribution 2')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the plot
plt.show()
```

Aus den über 14-Jährigen in Deutschland wird eine Person zufällig ausgewählt. Betrachtet werden folgende Ereignisse:

$M$: ..Die Person besitzt ein Mobiltelefon.“

$S$: „Die Person ist 65 Jahre oder älter “

$E$: „Mindestens eines der Ereignisse $M$ und $S$ tritt ein.“

### Teilaufgabe Teil B 1a (2 BE)

Geben Sie an, welche zwei der folgenden Mengen I bis VI jeweils das Ereignis $E$ beschreiben.
I $M \cap S$
II $\quad M \cup S$
III $\overline{M \cup S}$
IV $\quad(M \cap \bar{S}) \cup(\bar{M} \cap S) \cup(\bar{M} \cap \bar{S})$
v $(M \cap S) \cup(M \cap \bar{S}) \cup(\bar{M} \cap S)$
vi $\overline{M \cap S}$

### Lösung zu Teilaufgabe Teil B 1a

_**Ereignis beschreiben**_

Darstellung des Ereignisses $E$ in eine Vierfeldertafel:

|  | $\boldsymbol{M}$ | $\overline{\boldsymbol{M}}$ |  |
| :---: | :---: | :---: | :---: |
| $S$ | $M \cap S$ | $\bar{M} \cap S$ | $S$ |
| $\bar{S}$ | $M \cap \bar{S}$ | $\bar{M} \cap \bar{s}$ | $\bar{S}$ |
|  | $M$ | $\bar{M}$ | $\Omega$ |

$\Rightarrow \quad M \cup S \quad$ (Mengen II)

$\Rightarrow \quad(M \cap S) \cup(M \cap \bar{S}) \cup(\bar{M} \cap S) \quad$ (Mengen V)

#### Erläuterung: Ereignis

Das Ereignis $E$ : „Mindestens eines der Ereignisse $M$ und $S$ tritt ein.“ bedeutet:

Entweder es tritt $M$ und nicht $S$ ein $(M \cap \bar{S})$ oder es tritt $S$ und nicht $M$ ein $(S \cap \bar{M})$ oder es treten beide zusammen ein $(M \cap S$ ).

#### Erläuterung: Vereinigung zweier Ereignisse

|  | $\boldsymbol{M}$ | $\overline{\boldsymbol{M}}$ |  |
| :---: | :---: | :---: | :---: |
| $S$ | $M \cap S$ | $\bar{M} \cap S$ |   |
| $\bar{S}$ | $M \cap \bar{S}$ | $\bar{M} \cap \bar{s}$ |  |
|  |   |   |  |

Die violette schraffierte Fläche stellt die Vereinigung von $M$ und $S$ dar.

Bei der Vereinigung von zwei Ereignissen tritt entweder das eine oder das andere Ereignis ein.

#### Erläuterung:

An der Vierfeldertafel kann die schraffierte Menge direkt abgelesen werden.

### Teilaufgabe Teil B 1b (3 BE)

Entscheiden Sie anhand geeigneter Terme und auf der Grundlage der vorliegenden Daten, welche der beiden folgenden Wahrscheinlichkeiten größer ist. Begründen Sie Ihre Entscheidung.

$p_{1}$ ist die Wahrscheinlichkeit dafür, dass die ausgewählte Person ein Mobiltelefon besitzt, wenn bekannt ist, dass sie 65 Jahre oder älter ist.

$p_{2}$ ist die Wahrscheinlichkeit dafür, dass die ausgewählte Person 65 Jahre oder älter ist, wenn bekannt ist, dass sie ein Mobiltelefon besitzt.

### Lösung zu Teilaufgabe Teil B 1b

_**Bedingte Wahrscheinlichkeit**_

M: „Die Person besitzt ein Mobiltelefon."

$S$ : „Die Person ist 65 Jahre oder älter.“

$$
p_{1}=P_{S}(M)
$$

#### Erläuterung: Bedingte Wahrscheinlichkeit

Die Bezeichnung $P_{S}(M)$ bedeutet:

Die Wahrscheinlichkeit des Ereignisses $M$ unter der Bedingung, dass das Ereignis $S$ bereits eingetreten ist.

Diese Wahrscheinlichkeit heißt bedingte Wahrscheinlichkeit

#### Erläuterung: Bedingte Wahrscheinlichkeit

Die Bezeichnung $P_{M}(S)$ bedeutet:

Die Wahrscheinlichkeit des Ereignisses $S$ unter der Bedingung, dass das Ereignis $M$ bereits eingetreten ist.

Diese Wahrscheinlichkeit heißt bedingte Wahrscheinlichkeit.

$$
p_{2}=P_{M}(S)
$$

#### Erläuterung: Formel für die bedingte Wahrscheinlichkeit

$P_{A}(B)=\frac{P(A \cap B)}{P(A)}$

Die Wahrscheinlichkeit des Durchschnitts geteilt durch die Wahrscheinlichkeit der Bedingung.

Hinweis: $P(A \cap B)=P(B \cap A)$

$$
p_{1}=\frac{P(S \cap M)}{P(S)} ; \quad p_{2}=\frac{P(S \cap M)}{P(M)}
$$

#### Erläuterung:

Die Zähler von $p_{1}=\frac{P(S \cap M)}{P(S)}$ und $p_{2}=\frac{P(S \cap M)}{P(M)}$ sind gleich, also ist derjenige Bruch größer, der den kleineren Nenner hat.

Aus den Diagrammen der Teilaufgabe Teil B 1a entnimmt man, dass $P(S)=24 \%$ und $P(M)=90 \%$.

Somit gilt $P(S)<P(M)$ und demnach $p_{1}>p_{2}$.

Da $\underbrace{P(S)}_{0,24}<\underbrace{P(M)}_{0,9}$ gilt und die Zähler gleich sind, ist $p_{1}>p_{2}$.

### Teilaufgabe Teil B 1c (5 BE)

Erstellen Sie zu dem beschriebenen Sachverhalt für den Fall, dass das Ereignis $E$ mit einer Wahrscheinlichkeit von $98 \%$ eintritt, eine vollständig ausgefüllte Vierfeldertafel. Bestimmen Sie für diesen Fall die Wahrscheinlichkeit $P_{S}(M)$

### Lösung zu Teilaufgabe Teil B 1c

_**Vierfeldertafel für zwei Ereignisse**_

Aus Teilaufgabe Teil B 1a ist bekannt:

$P(M)=90 \%=0,9$

$P(S)=24 \%=0,24$

Für die Gegenereignisse ergibt sich somit:

$P(\bar{M})=1-0,9=0,1$

$P(\bar{S})=1-0,24=0,76$

Aus Teilaufgabe Teil B 1b ist weiterhin bekannt: $\quad P(E)=P(M \cup S)=0,98$

$\Rightarrow \quad P(\bar{M} \cap \bar{S})=1-0,98=0,02$

Werte in eine Vierfeldertafel eintragen:

|  | $\boldsymbol{M}$ | $\overline{\boldsymbol{M}}$ |  |
| :---: | :---: | :---: | :---: |
| $\boldsymbol{S}$ |  |  | 0,24 |
| $\overline{\boldsymbol{S}}$ |  | 0,02 | 0,76 |
|  | 0,9 | 0,1 | 1 |

Vierfeldertafel vervollständigen:

|  | $\boldsymbol{M}$ | $\overline{\boldsymbol{M}}$ |  |
| :---: | :---: | :---: | :---: |
| $\boldsymbol{S}$ | 0,16 | 0,08 | 0,24 |
| $\overline{\boldsymbol{S}}$ | 0,74 | 0,02 | 0,76 |
|  | 0,9 | 0,1 | 1 |

_**Bedingte Wahrscheinlichkeit**_

$$
P_{S}(M)=\frac{P(S \cap M)}{P(S)}=\frac{0,16}{0,24}=\frac{16}{24}=\frac{2}{3}
$$

#### Erläuterung: Formel für die bedingte Wahrscheinlichkeit

$$
P_{A}(B)=\frac{P(A \cap B)}{P(A)}
$$

Die Wahrscheinlichkeit des Durchschnitts geteilt durch die Wahrscheinlichkeit der Bedingung.

Hinweis: $P(A \cap B)=P(B \cap A)$

## Aufgabe B 2
Zwei Drittel der Senioren in Deutschland besitzen ein Mobiltelefon. Bei einer Talkshow
zum Thema „Chancen und Risiken der digitalen Welt" sitzen 30 Senioren im Publikum.

### Teilaufgabe Teil B 2a (3 BE)


Bestimmen Sie die Wahrscheinlichkeit dafür, dass unter 30 zufällig ausgewählten Senioren in Deutschland mindestens 17 und höchstens 23 ein Mobiltelefon besitzen.

### Lösung zu Teilaufgabe Teil B 2a

_**Binomialverteilung**_

Ereignis $A$ : „Unter 30 Senioren besitzen mindestens 17 und höchstens 23 ein Mobiltelefon“ $p=P($, ,Senior besitzt ein Mobiltelefon“ $)=\frac{2}{3}$

Bernoulli-Kette mit $n=30$ und $p=\frac{2}{3}$.

$$
P(A)=P_{\frac{2}{3}}^{30}(17 \leq X \leq 23)
$$

$P(A)=P_{\frac{2}{3}}^{30}(X \leq 23)-P_{\frac{2}{3}}^{30}(X \leq 16)$

(Werte werden aus dem stochastischen Tafelwerk entnommen)

$P(A) \approx 0,91616-0,08977$

$P(A) \approx 82,6 \%$

#### Erläuterung: Bernoulli-Kette

Ein Zufallsexperiment mit zwei möglichen Ausgängen (Treffer, Niete) nennt man Bernoulli-Experiment
$p$
$q=1-p$
Wahrscheinlichkeit für einen Treffe
Wahrscheinlichkeit für eine Niete
hier : $p=\frac{2}{3}$
hier : $q=\frac{1}{3}$

In diesem Fall ist ein Senior mit ein Mobiltelefon ein Treffer.

Bei mehrmaligem Ziehen in einem Bernoulli-Experiment spricht man von einer Bernoulli-Kette.

$n \quad$ Anzahl der Züge („Länge“ der Bernoulli-Kette) hier : $n=30$


#### Erläuterung: Ereignis

“... mindestens 17 und höchstens 23 ..." $\Rightarrow \quad 17 \leq X \leq 23$


#### Erläuterung: Bernoulli-Formel

Wenn die Zufallsvariable $X$ zwischen zwei Zahlen $a$ und $b$ liegen soll, dann gilt:

$P(a \leq X \leq b)=P(X \leq b)-P(X \leq a-1)$

„Obere Grenze minus die um 1 verkleinerte untere Grenze“

```
0                16  17             23
|----------------|---|--------------|---|
                        P(17≤X≤23)

|-----------------------------------|
                 P(X≤23)

|----------------|
    P(X≤16)
```


### Teilaufgabe Teil B 2b (3 BE)
Von den 30 Senioren im Publikum besitzen 24 ein Mobiltelefon. Im Verlauf der Sendung werden drei der Senioren aus dem Publikum zufällig ausgewählt und nach ihrer Meinung befragt.

Bestimmen Sie die Wahrscheinlichkeit dafür, dass genau zwei dieser drei Senioren ein Mobiltelefon besitzen.

### Lösung zu Teilaufgabe Teil B 2b

_**Ziehen ohne Reihenfolge ohne Zurücklegen**_

$E:$, 2 von 3 Senioren besitzen ein Mobiltelefon

$P(E)=\frac{\left(\begin{array}{c}24 \\ 2\end{array}\right) \cdot\left(\begin{array}{c}6 \\ 1\end{array}\right)}{\left(\begin{array}{c}30 \\ 3\end{array}\right)} \approx 40,8 \%$

#### Erläuterung: Ziehen ohne Reihenfolge und ohne Zurücklegen

Es handelt sich hier um Ziehen ohne Reihenfolge (welcher Senior wann befragt wir ist irrelevant) und ohne Zurücklegen (eine Person wird nur einmal befragt).

Stichwort: „Lottoprinzip“ bzw. hypergeometrische Verteilung:

$P(X)=\frac{\text { Anzahl Treffer } \cdot \text { Anzahl Nieten }}{|\Omega|}$

2 Senioren mit Mobiltelefon (aus den möglichen 24) werden ausgewählt

$\Rightarrow \mid$ Treffer $\left\lvert\,=\left(\begin{array}{c}24 \\ 2\end{array}\right)\right.$

1 Senior ohne Mobiltelefon (aus den übrigen 6) werden ausgewählt

$\Rightarrow \mid$ Niete $\left\lvert\,=\left(\begin{array}{l}6 \\ 1\end{array}\right)\right.$

3 Senioren werden aus 30 gezogen:

$\Rightarrow|\Omega|=\left(\begin{array}{c}30 \\ 3\end{array}\right)$

Merkhilfe zur Kontrolle:

$\left(\begin{array}{c}24 \\ 2\end{array}\right)\left|\left(\begin{array}{l}6 \\ 1\end{array}\right)\right|\left(\begin{array}{c}30 \\ 3\end{array}\right)$


## Aufgabe B 3
Eine Handelskette hat noch zahlreiche Smartphones des Modells $Y 3$ auf Lager, als der Hersteller das Nachfolgemodell $Y 4$ auf den Markt bringt. Der Einkaufspreis für das neue $Y 4$ beträgt $300 €$, während die Handelskette für das Vorgängermodell $Y 3$ im Einkauf nur $250 €$ bezahlen musste. Um die Lagerbestände noch zu verkaufen, bietet die Handelskette ab dem Verkaufsstart des $Y 4$ die Smartphones des Typs $Y 3$ für je $199 €$ an.

### Teilaufgabe Teil B 3 (4 BE)


Aufgrund früherer Erfahrungen geht die Handelskette davon aus, dass von den verkauften Smartphones der Modelle $Y 3$ und $Y 4$ trotz des Preisnachlasses nur $26 \%$ vom Typ $Y 3$ sein werden. Berechnen Sie unter dieser Voraussetzung, zu welchem Preis die Handelskette das $Y 4$ anbieten muss, damit sie voraussichtlich pro verkauftem Smartphone der Modelle Y3 und $Y 4 \mathrm{im}$ Mittel $97 €$ mehr erhält, als sie beim Einkauf dafür zahlen musste.

### Lösung zu Teilaufgabe Teil B 3

_**Erwartungswert einer Zufallsgröße**_

$P($,Verkauft wurde ein $\mathrm{Y} 3 “)=0,26$

$P($, Verkauft wurde ein $Y 4 ")=1-0,26=0,74$

| $x_{i}$ | $Y 3$ | $Y 4$ |
| :---: | :---: | :---: |
| $p_{i}=P\left(X=x_{i}\right)$ | 0,26 | 0,74 |
| Kosten $K\left(x_{i}\right)$ | $250 €$ | $300 €$ |
| Verkaufspreis $V\left(x_{i}\right)$ | $199 €$ | $x$ |

Im Mittel zu erwartende Kosten bestimmen:

$E(K)=0,26 \cdot 250+0,74 \cdot 300=287 €$

$E(V)=0,26 \cdot 199+0,74 \cdot x$

Es soll gelten: $\quad E(V)=E(K)+97=287+97=384 €$

Einsetzen in $E(V)$ und nach $x$ auflösen

$384=0,26 \cdot 199+0,74 \cdot x$

$x=\frac{384-0,26 \cdot 199}{0,74}=449 €$


#### Erläuterung: Erwartungswert einer Zufallsgröß

Der Erwartungswert einer Zufallsgröße $X$ (hier $K$ ) bei $n$ Versuchen (hier 2), ist definiert als:

$$
E_{n}(X)=\sum_{i=1}^{n} x_{i} \cdot P\left(X=x_{i}\right)
$$

In diesem Fall:

$$
E(K)=\sum_{i=1}^{2} K\left(x_{i}\right) \cdot P\left(X=x_{i}\right)
$$

Im Mittel zu erwartende Einnahmen $V$ bestimmen:

#### Erläuterung: Erwartungswert einer Zufallsgröß

Der Erwartungswert einer Zufallsgröße $X$ (hier $V$ ) bei $n$ Versuchen (hier 2), ist definiert als:

$E_{n}(X)=\sum_{i=1}^{n} x_{i} \cdot P\left(X=x_{i}\right)$

In diesem Fall:

$E(V)=\sum_{i=1}^{2} V\left(x_{i}\right) \cdot P\left(X=x_{i}\right)$
