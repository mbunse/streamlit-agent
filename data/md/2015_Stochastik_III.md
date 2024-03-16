# Abitur 2015 Mathematik Stochastik III

## Aufgabe A 1

Bei der Wintersportart Biathlon wird bei jeder Schießeinlage auf fünf Scheiben geschossen. Ein Biathlet tritt bei einem Einzelrennen zu einer Schießeinlage an, bei der er auf jede Scheibe einen Schuss abgibt. Diese Schießeinlage wird modellhaft durch eine Bernoulikette mit der Länge 5 und der Trefferwahrscheinlichkeit $p$ beschrieben.

### Teilaufgabe Teil A 1a (3 BE)

Geben Sie für die folgenden Ereignisse $A$ und $B$ jeweils einen Term an, der die Wahrscheinlichkeit des Ereignisses in Abhängigkeit von $p$ beschreibt.

A: „Der Biathlet trifft bei genau vier Schüssen.“

B: „Der Biathlet trifft nur bei den ersten beiden Schüssen."

### Lösung zu Teilaufgabe Teil A 1

_**Binomialverteilung**_

A: „Der Biathlet trifft bei genau vier Schüssen.“

$n=5$

$k=4$

$P(A)=P_{p}^{5}(Z=4)=\left(\begin{array}{l}5 \\ 4\end{array}\right) \cdot p^{4} \cdot(1-p)$

B: „Der Biathlet trifft nur bei den ersten beiden Schüssen."

$P(B)=p^{2} \cdot(1-p)^{3}$

#### Erläuterung: Bernoulli-Formel

Die Wahrscheinlichkeit genau $k$ Treffer bei $n$ Versuchen zu erzielen beträgt:

$P(\mathrm{k}$ Treffer $)=P_{p}^{n}(Z=k)=\left(\begin{array}{l}n \\ k\end{array}\right) \cdot p^{k} \cdot(1-p)^{n-k}$

Dabei ist:

$n=$ Anzahl der Versuch

$k=$ Anzahl der Treffer

$p=$ Wahrscheinlichkeit eines Treffers pro Versuch

$1-p=$ Wahrscheinlichkeit einer Niete pro Versuch

#### Erläuterung: Wahrscheinlichkeit

Veranschaulichung des Ereignisses:

| $T$ | $T$ | $\bar{T}$ | $\bar{T}$ | $\bar{T}$ |
| --- | --- | --------- | --------- | --------- |
| 1   | 2   | 3         | 4         | 5         |

$p=$ Wahrscheinlichkeit eines Treffers $(T)$ pro Versuch

$1-p=$ Wahrscheinlichkeit einer Niete $(\bar{T})$ pro Versuch

$P(B)=p \cdot p \cdot(1-p) \cdot(1-p) \cdot(1-p)=p^{2} \cdot(1-p)^{3}$

### Teilaufgabe Teil A 1b (2 BE)

Erläutern Sie anhand eines Beispiels, dass die modellhafte Beschreibung der Schießeinlage durch eine Bernoullikette unter Umständen der Realität nicht gerecht wird.

### Lösung zu Teilaufgabe Teil A 1b

_**Binomialverteilung**_

Z. B.:

Der Biathlet verfehlt einen Schuss und wird nervös. Die Trefferwahrscheinlichkeit beim nächsten Schuss ist beeinflusst und sinkt.

## Aufgabe A 2

Ein Moderator lädt zu einer Talkshow drei Politiker, eine Journalistin und zwei Mitglieder einer Bürgerinitiative ein. Für die Diskussionsrunde ist eine halbkreisförmige Sitzordnung vorgesehen, bei der nach den Personen unterschieden wird und der Moderator den mittleren einnimmt.

### Teilaufgabe Teil A 2a (1 BE)

Geben Sie einen Term an, mit dem die Anzahl der möglichen Sitzordnungen berechnet werden kann, wenn keine weiteren Einschränkungen berücksichtigt werden.

### Lösung zu Teilaufgabe Teil A 2

_**Kombinatorik**_

| - | - | - | M | - | - | - |
| --- | --- | --- | --- | --- | ---| --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |

$6 !$

#### Erläuterung: Permutation

3 Politiker +1 Journalisten +2 Mitglieder einer Bürgerinitiative $=6$ Personen.

Der Moderator hat einen festen Platz und muss somit nicht berücksichtigt werden.

Es gibt 6! Möglichkeiten 6 Personen auf 6 Plätze zu verteilen.


### Teilaufgabe Teil A 2b (4 BE)

Der Sender hat festgelegt, dass unmittelbar neben dem Moderator auf einer Seite die Journalistin und auf der anderen Seite einer der Politiker sitzen soll. Berechnen Sie unter Berücksichtigung dieser weiteren Einschränkung die Anzahl der möglichen Sitzordnungen.

### Lösung zu Teilaufgabe Teil A 2b

_**Kombinatorik**_

| - | - | J | M | P | - | - |
| --- | --- | --- | --- | --- | ---| --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |

$$
\underbrace{2}_{J} \cdot \underbrace{3}_{P} \cdot \underbrace{4 !}_{\text {Rest }}=144
$$

#### Erläuterung: Permutation

Die Journalistin (J) und einer der Politiker (P) sitzen unmittelbar neben dem Moderator (M).

J kann entweder rechts oder links vom Moderator sitzen, also gibt es 2 Möglichkeiten.

Ist der Platz für $\mathrm{J}$ fest, so gibt es 3 Möglichkeiten einen Politiker auf den anderen Platz neben dem Moderator zu platzieren.

Auf den anderen 4 Plätzen müssen 4 Personen verteilt werden. Hierfür gibt 4! Möglichkeiten.

## Aufgabe B 1
Der Marketingchef einer Handelskette plant eine Werbeaktion, bei der ein Kunde die Höhe des Rabatts bei seinem Einkauf durch zweimaliges Drehen an einem Glücksrad selbst bestimmen kann. Das Glücksrad hat zwei Sektoren, die mit den Zahlen 5 bzw. 2 beschriftet sind (vgl. Abbildung).

Der Rabatt in Prozent errechnet sich als Produkt der beiden Zahlen, die der Kunde bei zweimaligem Drehen am Glücksrad erzielt.

Die Zufallsgröße $X$ beschreibt die Höhe dieses Rabatts in Prozent, kann also die Werte 4, 10 oder 25 annehmen. Die Zahl 5 wird beim Drehen des Glücksrads mit der Wahrscheinlichkeit $p$ erzielt.

Vereinfachend soll davon ausgegangen werden, dass jeder Kunde genau einen Einkauf tätigt und auch tatsächlich am Glücksrad dreht.

### Teilaufgabe Teil B 1a (3 BE)

```python
import matplotlib.pyplot as plt

# The values for each segment
sizes = [5, 2]

# The labels for each segment
labels = ['5', '2']

# The explode (offset) for the arrowed segment, assuming the arrow points to the first segment
explode = [0.1, 0]  # only "explode" the 1st slice (i.e. '5')

# Create a pie chart
plt.figure(figsize=(6, 4))
plt.pie(sizes, labels=labels, explode=explode, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the plot
plt.show()
```

Ermitteln Sie mithilfe eines Baumdiagramms die Wahrscheinlichkeit dafür, dass ein Kunde bei seinem Einkauf einen Rabatt von $10 \%$ erhält.

(Ergebnis: $2 p-2 p^{2}$ )

### Lösung zu Teilaufgabe Teil B 1a

_**Wahrscheinlichkeit**_

Baumdiagramm zeichnen:

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Function to create a rectangle with text inside, representing a decision or an endpoint
def create_rectangle(ax, center, width, height, text):
    rect = patches.Rectangle((center[0] - width / 2, center[1] - height / 2), width, height, linewidth=1, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    plt.text(center[0], center[1], text, ha='center', va='center')

# Start plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 30)
ax.set_ylim(0, 10)
ax.axis('off') # Hide the axes

# Draw rectangles and connectors
create_rectangle(ax, (5, 8), 4, 1, '5')
create_rectangle(ax, (15, 9), 4, 1, '5')
create_rectangle(ax, (25, 9), 4, 1, '25')
create_rectangle(ax, (15, 6), 4, 1, '2')
create_rectangle(ax, (25, 6), 4, 1, '10')
create_rectangle(ax, (5, 3), 4, 1, '2')
create_rectangle(ax, (15, 4), 4, 1, '5')
create_rectangle(ax, (25, 4), 4, 1, '10')
create_rectangle(ax, (15, 1), 4, 1, '2')
create_rectangle(ax, (25, 1), 4, 1, '4')

# Draw connectors
plt.plot([5, 15], [8, 9], 'k-', lw=1)
plt.plot([15, 25], [9, 9], 'k-', lw=1)
plt.plot([5, 15], [8, 6], 'k-', lw=1)
plt.plot([15, 25], [6, 6], 'k-', lw=1)
plt.plot([5, 5], [8, 3], 'k-', lw=1)
plt.plot([5, 15], [3, 4], 'k-', lw=1)
plt.plot([15, 25], [4, 4], 'k-', lw=1)
plt.plot([5, 15], [3, 1], 'k-', lw=1)
plt.plot([15, 25], [1, 1], 'k-', lw=1)

# Draw probability texts
plt.text(10, 8.5, 'p', ha='center', va='center')
plt.text(10, 7.5, '1-p', ha='center', va='center')
plt.text(20, 9.5, 'p', ha='center', va='center')
plt.text(20, 6.5, '1-p', ha='center', va='center')
plt.text(10, 3.5, 'p', ha='center', va='center')
plt.text(10, 2.5, '1-p', ha='center', va='center')
plt.text(20, 4.5, 'p', ha='center', va='center')
plt.text(20, 1.5, '1-p', ha='center', va='center')

# Show the plot
plt.show()
```

#### Erläuterung: 1. Pfadregel, 2. Pfadregel

1. Pfadregel: In einem Baumdiagramm ist die Wahrscheinlichkeit eines Ereignisse gleich dem Produkt der Wahrscheinlichkeiten längs des zugehörigen Pfades.

In diesem Fall:

$P(5 \cap 2)=P(5) \cdot P_{5}(2)=p \cdot(1-p)$

$P(2 \cap 5)=P(2) \cdot P_{2}(5)=(1-p) \cdot p$

2. Pfadregel: In einem Baumdiagramm ist die Wahrscheinlichkeit eines Ereignisse gleich der Summe der für dieses Ereignis zugehörigen Pfadwahrscheinlichkeiten.

In diesem Fall: $\quad P(10 \%$ Rabatt $)=P(5 \cap 2)+P(2 \cap 5$

$P(10 \%$ Rabatt $)=p \cdot(1-p)+(1-p) \cdot p$

$P(10 \%$ Rabatt $)=p-p^{2}+p-p^{2}$

$P(10 \%$ Rabatt $)=2 p-2 p^{2}$

### Teilaufgabe Teil B 1b (3 BE)

Zeigen Sie, dass für den Erwartungswert $E(X)$ der Zufallsgröße $X$ gilt: $E(X)=9 p^{2}+12 p+4$

### Lösung zu Teilaufgabe Teil B 1b

#### Erwartungswert einer Zufallsgröße

Tabelle der Wahrscheinlichkeitsverteilung erstellen:
Erläuterung: Wahrscheinlichkeit

Mit dem Baumdiagramm aus Teil B Teilaufgabe 1a können die einzelnen Wahrscheinlichkeiten bestimmt werden:

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Function to create a rectangle with text inside, representing a decision or an endpoint
def create_rectangle(ax, center, width, height, text):
    rect = patches.Rectangle((center[0] - width / 2, center[1] - height / 2), width, height, linewidth=1, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    plt.text(center[0], center[1], text, ha='center', va='center')

# Start plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 30)
ax.set_ylim(0, 10)
ax.axis('off') # Hide the axes

# Draw rectangles and connectors
create_rectangle(ax, (5, 8), 4, 1, '5')
create_rectangle(ax, (15, 9), 4, 1, '5')
create_rectangle(ax, (25, 9), 4, 1, '25')
create_rectangle(ax, (15, 6), 4, 1, '2')
create_rectangle(ax, (25, 6), 4, 1, '10')
create_rectangle(ax, (5, 3), 4, 1, '2')
create_rectangle(ax, (15, 4), 4, 1, '5')
create_rectangle(ax, (25, 4), 4, 1, '10')
create_rectangle(ax, (15, 1), 4, 1, '2')
create_rectangle(ax, (25, 1), 4, 1, '4')

# Draw connectors
plt.plot([5, 15], [8, 9], 'k-', lw=1)
plt.plot([15, 25], [9, 9], 'k-', lw=1)
plt.plot([5, 15], [8, 6], 'k-', lw=1)
plt.plot([15, 25], [6, 6], 'k-', lw=1)
plt.plot([5, 5], [8, 3], 'k-', lw=1)
plt.plot([5, 15], [3, 4], 'k-', lw=1)
plt.plot([15, 25], [4, 4], 'k-', lw=1)
plt.plot([5, 15], [3, 1], 'k-', lw=1)
plt.plot([15, 25], [1, 1], 'k-', lw=1)

# Draw probability texts
plt.text(10, 8.5, 'p', ha='center', va='center')
plt.text(10, 7.5, '1-p', ha='center', va='center')
plt.text(20, 9.5, 'p', ha='center', va='center')
plt.text(20, 6.5, '1-p', ha='center', va='center')
plt.text(10, 3.5, 'p', ha='center', va='center')
plt.text(10, 2.5, '1-p', ha='center', va='center')
plt.text(20, 4.5, 'p', ha='center', va='center')
plt.text(20, 1.5, '1-p', ha='center', va='center')

# Show the plot
plt.show()
```

$P(X=4)=(1-p)(1-p)=(1-p)^{2}$

$P(X=10)=2 p-2 p^{2} \quad$ (s. Teil B Teilaufgabe 1a)

$P(X=25)=p \cdot p=p^{2}$

$$
\begin{array}{c|c|c|c}
x_{i} & 4 & 10 & 25 \\
\hline P\left(X=x_{i}\right) & (1-p)^{2} & 2 p-2 p^{2} & p^{2}
\end{array}
$$

Erwartungswert $E(X)$ bestimmen:

Erläuterung: Erwartungswert einer Zufallsgröß

Der Erwartungswert einer Zufallsgröße $X$ bei $n$ Versuchen (hier 3), ist definiert als:

$E_{n}(X)=\sum_{i=1}^{n} x_{i} \cdot P\left(X=x_{i}\right)$

In diesem Fall:

$E(X)=\sum_{i=1}^{3} x_{i} \cdot P\left(X=x_{i}\right)$

$E(X)=4 \cdot(1-p)^{2}+10 \cdot\left(2 p-2 p^{2}\right)+25 \cdot p^{2}$

$E(X)=4-8 p+4 p^{2}+20 p-20 p^{2}+25 p^{2}$

$E(X)=9 p^{2}+12 p+4$

### Teilaufgabe Teil B 1c (3 BE)

Die Geschäftsführung will im Mittel für einen Einkauf einen Rabatt von $16 \%$ gewähren. Berechnen Sie für diese Vorgabe den Wert der Wahrscheinlichkeit $p$.

### Lösung zu Teilaufgabe Teil B 1

_**Quadratische Gleichung**_

$E(X)=16$

$9 p^{2}+12 p+4=16$

$9 p^{2}+12 p-12=0$

$p_{1,2}=\frac{-12 \pm \sqrt{144-4 \cdot 9 \cdot(-12)}}{2 \cdot 9}$

$p_{1,2}=\frac{-12 \pm 24}{18}$

Erläuterung: Wahrscheinlichkeit

$p$ kann nur Werte zwischen 0 und 1 annehmen, deswegen ist $p_{2}=-2$ auszuschließen. $\Rightarrow \quad p_{1}=\frac{2}{3}$

$\left(p_{2}=-2\right)$

### Teilaufgabe Teil B 1d (4 BE)

Die Wahrscheinlichkeit, dass ein Kunde bei seinem Einkauf den niedrigsten Rabatt erhält, beträgt $\frac{1}{9}$. Bestimmen Sie, wie viele Kunden mindestens an dem Glücksrad drehen müssen, damit mit einer Wahrscheinlichkeit von mehr als $99 \%$ mindestens einer der Kunden den niedrigsten Rabatt erhält.

### Lösung zu Teilaufgabe Teil B 1d

_**Binomialverteilung**_

Text analysieren

$p(,$, Kunde erhält niedrigsten Rabatt" $)=\frac{1}{9}$

"... wie viele Kunden ..." $\Rightarrow \quad n$ ist gesucht

“... mindestens einer der Kunden..." $\Rightarrow \quad X \geq 1$

"...mit einer Wahrscheinlichkeit von mehr als $99 \%$..." $\Rightarrow \quad P>0,99$

Es muss also gelten:

$P_{\frac{1}{9}}^{n}(X \geq 1)>0,99$

$P($ mind. 1 Treffer $)=1-P($ kein Treffer

$1-P_{\frac{1}{9}}^{n}(X=0)>0,99$

$1-\left(\frac{8}{9}\right)^{n}>0,99$

$n>\frac{\ln (1-0,99)}{\ln \left(\frac{8}{9}\right)} \approx 39,1$

$\Rightarrow \quad n \geq 40$ (Kunden)

#### Erläuterung: Bernoulli-Kette

Das Zufallsexperiment kann als Bernoulli-Kette der Länge $n$ mit der Trefferwahrscheinlichkeit $p=\frac{1}{9}$ angesehen werden.

#### Erläuterung: Gegenereignis

Wahrscheinlichkeiten des Typs $P$ (mind. 1 Treffer) können meist leicht über das Gegenereignis bestimmt werden.

#### Erläuterung: Bernoulli-Formel

Die Wahrscheinlichkeit genau $k$ Treffer bei $n$ Versuchen zu erzielen beträgt:

$P(\mathrm{k}$ Treffer $)=P_{p}^{n}(Z=k)=\left(\begin{array}{l}n \\ k\end{array}\right) \cdot p^{k} \cdot(1-p)^{n-k}$

Dabei ist:

$n=$ Anzahl der Versuche

$k=$ Anzahl der Treffer

$p=$ Wahrscheinlichkeit eines Treffers pro Versuch

$1-p=$ Wahrscheinlichkeit einer Niete pro Versuch

Spezialfall $k=0$

$P(0$ Treffer $)=P_{p}^{n}(Z=0)=\underbrace{\left(\begin{array}{l}n \\ 0\end{array}\right)}_{1} \cdot \underbrace{p^{0}}_{1} \cdot(1-p)^{n-0}$

$\Rightarrow P(0$ Treffer $)=(1-p)^{n}$

#### Erläuterung: Rechenweg

$1-\left(\frac{8}{9}\right)^{n}>0,99 \quad \mid \quad$ umstellen

$\left(\frac{8}{9}\right)^{n}<1-0,99 \quad \mid \quad$ logarithmieren

$\ln \left(\frac{8}{9}\right)^{n}<\ln (1-0,99)$

$n \cdot \ln \left(\frac{8}{9}\right)<\ln (1-0,99)$

(da die Ungleichung durch eine negative Zahl geteilt wird, ändert sich das Relationszeichen)

$n>\frac{\ln (1-0,99)}{\ln \left(\frac{8}{9}\right)}$

## Aufgabe B 2
Eine der Filialen der Handelskette befindet sich in einem Einkaufszentrum, das zu Werbezwecken die Erstellung einer Smartphone-App in Auftrag geben will. Diese App soll die Kunden beim Betreten des Einkaufszentrums über aktuelle Angebote und Rabattaktionen der beteiligten Geschäfte informieren. Da dies mit Kosten verbunden ist, will der Finanzchef der Handelskette einer Beteiligung an der App nur zustimmen, wenn mindestens 15\% der Kunden der Filiale bereit sind, diese App zu nutzen. Der Marketingchef warnt jedoch davor, auf eine Beteiligung an der App zu verzichten, da dies zu einem Imageverlust führen könnte.

### Teilaufgabe Teil B 2a (4 BE)


Um zu einer Entscheidung zu gelangen, will die Geschäftsführung der Handelskette eine der beiden folgenden Nullhypothesen auf der Basis einer Befragung von 200 Kunden auf einem Signifikanzniveau von $10 \%$ testen:

I "Weniger als 15\% der Kunden sind bereit, die App zu nutzen."

II "Mindestens $15 \%$ der Kunden sind bereit, die App zu nutzen."

Nach Abwägung der möglichen Folgen, die der Finanzchef und der Marketingchef aufgezeigt haben, wählt die Geschäftsführung für den Test die Nullhypothese II. Bestimmen Sie die zugehörige Entscheidungsregel.

### Lösung zu Teilaufgabe Teil B 2a

_**Hypothesentest - Fehler erster Art**_

Text analysieren und Daten herauslesen:

Nullhypothese: $\quad H_{0}: p \geq 0,15$

Stichprobenumfang: $\quad n=200$

Signifikanzniveau: $\quad \alpha=10 \%$

Annahmebereich von $H_{0}: \quad A=[k+1,200]$

Ablehnungsbereich von $H_{0}: \quad \bar{A}=[0, k]$

```
0                   k k+1              n=200
|-------------------| |--------------------|
  Ablehnungsbereich       Annahmebereich
```
Fehler 1. Art bestimmen:

$\quad P_{0,15}^{200}(Z \leq k) \leq 0,10$

Aus dem Tafelwerk ablesen: $k\leq 23$

Entscheidungsregel:


```
0                   23 24              n=200
|-------------------| |--------------------|
  Ablehnungsbereich       Annahmebereich
```

#### Erläuterung: Nullhypothese

Da hier die Nullhypothese " $p \geq 0,15$ " bzw. " Mindestens $15 \%$ " lautet, liegt der Annahmebereich rechts und der Ablehnungsbereich links.

![](https://cdn.mathpix.com/cropped/2024_03_15_fe47d1185a2f640ab34ag-8.jpg?height=103&width=699&top_left_y=1138&top_left_x=389)


#### Erläuterung: Fehler 1.Art

Man spricht von „Fehler 1. Art“, wenn die Nullhypothese fälschlicherweise abgelehnt wird.

Das ist der Fall, wenn $H_{0}$ wahr ist, man sich aber gegen $H_{0}$ entscheidet, da das Stichprobenergebnis zufällig im Ablehnungsbereich liegt ( $Z \leq k$ ).

$\Rightarrow \quad$ Fehler erster Art: $\quad P_{0,15}^{200}(Z \leq k) \leq 0,10$


### Teilaufgabe Teil B 2b (3 BE)

Entscheiden Sie, ob bei der Abwägung, die zur Wahl der Nullhypothese II führte, die Befürchtung eines Imageverlusts oder die Kostenfrage als schwerwiegender erachtet wurde. Erläutern Sie Ihre Entscheidung.

### Lösung zu Teilaufgabe Teil B 2b

_**Hypothesentest - Fehler erster Art**_

Befürchtung eines Imageverlusts.

Begründung:

Das Risiko, fälschlicherweise die Nullhypothese zu verwerfen, also irrtümlich sich gegen die Beiteilung zu entscheiden und somit den Imageverlust in Kauf nehmen, ist mit 10\% rech niedrig.
