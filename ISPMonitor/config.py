import os

base_path = os.path.join(os.path.dirname(__file__))

# Internet Speeds
down_speed = 100.0
up_speed = 100.0

provider = '@xxx'

telegram_message = """
Actualmente la calidad de la conexión es:
    - Velocidad de bajada⬇: {down:.2f} Mbps
    - Velocidad de subida⬆: {up:.2f} Mbps
    - Latencia: {ping:.2f} ms
    - Conectado durante: {uptime}
    - Ratio de lo contratado: {ratio:.2f}%
    - Comentario: {reaction}
"""


messages = dict(
    awesome='Increíble',
    great='Genial',
    fair='Buena',
    mediocre='Regular',
    bad='Mala',
    terrible='Terrible',
    illegal='Ilegal'
)

movistar = {
    'down_ratio': 0.4,
    'up_ratio': 0.4,
    'ping': 80,
    'online': 0.995,
}