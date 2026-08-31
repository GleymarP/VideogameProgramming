### Power-up: Heavy Ball 

#### Descripción General
El **Heavy Ball** es un power-up ofensivo diseñado para acelerar la destrucción de bloques de alta resistencia en niveles avanzados. Transforma las pelotas activas en "heavy balls", permitiendo que ignoren la durabilidad de los ladrillos con capas múltiples y reduzcan su nivel de dureza.

---

#### Mecánica y Comportamiento
1. **Recolección:** Al colisionar la paleta con el power-up, se reproduce un sonido y se activa el estado `heavy = True` en todas las pelotas en juego.
2. **Efecto de Impacto:** Cuando una pelota en estado *Heavy* colisiona contra cualquier ladrillo con un nivel de durabilidad superior a cero (`brick.tier > 0`), reduce automáticamente su nivel a `tier = 0`. Esto permite destruir ladrillos dorados o reforzados de un solo golpe adicional.
3. **Duración:** El efecto es temporal y dura **8.0 segundos**, administrado mediante `gale.timer.Timer`. Una vez vencido el tiempo, las pelotas regresan a su estado normal.

---

#### Detalles 
* **Clase `HeavyBall`:** Subclase de `PowerUp`. Utiliza `Timer.after(8.0, deactivate_heavy)`.
* **Integración en `PlayState.py`:**  En la fase de actualización (`update`), se verifica si la pelota colisionada tiene el atributo `heavy` activo. Si se cumple y brick.tier > 0, fuerza `brick.tier = 0` justo antes de ejecutar el método `brick.hit()`.
* **Condición:**  Para mantener el balance del juego, el power-up  se agrega únicamente a partir del **Nivel 2**.