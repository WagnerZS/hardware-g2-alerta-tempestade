# Arduino Monitor

Servidor Python para receber leituras JSON de um Arduino pela porta serial, aplicar uma regra de alerta e disponibilizar os dados por REST API. O projeto foi organizado para execução em uma Raspberry Pi 4.

## Estrutura

```text
arduino-monitor/
├── api/                 # FastAPI, rotas e configurações
├── cli/                 # ponto de entrada do servidor
├── domain/              # modelos Pydantic, regra e serviço
├── infra/               # integração com a porta serial
├── web/static/          # reservado para HTML, CSS e JavaScript do painel
├── tests/
├── .env.example
└── pyproject.toml
```

## Contrato serial

O Arduino deve enviar uma linha JSON por leitura, terminada por `\\n`:

```json
{"temp": 27.4, "umid": 36.5, "mag": 812}
```

Todos os três atributos são numéricos. Para cada leitura:

- `gravidade = "ALERTA"` quando `umid >= 35.0 AND mag >= 800`;
- caso contrário, `gravidade = "NORMAL"`;
- quando a condição de alerta é verdadeira, o servidor responde na serial com `ALERTA\\n`;
- a leitura processada fica disponível em `GET /api/v1/leituras/ultima`.

## Instalação com uv

```bash
uv venv
source .venv/bin/activate
uv sync --extra dev
cp .env.example .env
```

Ajuste `SERIAL_PORT` no `.env` conforme a Raspberry Pi, normalmente `/dev/ttyACM0` ou `/dev/ttyUSB0`.

## Execução

```bash
uv run arduino-monitor
# ou
uv run uvicorn api.app:app --host 0.0.0.0 --port 8000
```

A documentação interativa fica em `http://<ip-da-raspberry>:8000/docs`.

## API

Enviar uma leitura manualmente:

```bash
curl -X POST http://localhost:8000/api/v1/leituras \\
  -H 'Content-Type: application/json' \\
  -d '{"temp":27.4,"umid":36.5,"mag":812}'
```

Consultar a última leitura:

```bash
curl http://localhost:8000/api/v1/leituras/ultima
```

O painel web ainda não foi criado, conforme solicitado. Os arquivos estáticos deverão ser colocados em `web/static`, podendo ser consumidos pelo navegador em `/static/...`.

## Permissão da serial na Raspberry Pi

Caso o processo não consiga abrir a porta, inclua o usuário no grupo serial e reinicie a sessão:

```bash
sudo usermod -aG dialout "$USER"
```
