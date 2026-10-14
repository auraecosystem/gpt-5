#8 ERROR: failed to calculate checksum of ref ... "/go.sum": not found
https://github.com/web4hub/gpt-5-mini.git
cd gpt-5-mini
python -m venv myenv
myenv\Scripts\activate
source myenv/bin/activate
pip install -r requirements.txt
go mod tidy
ls -la go.mod go.sum
cat .dockerignore
docker build -t myapp .
ls -la
cat go.mod
cat go.sum
ls -la
cat go.mod
cat go.sum
docker build -f deploy/Dockerfile -t app .
app/
  go.mod
  go.sum
  main.go
  cmd/
  internal/
  deploy/
    Dockerfile
    backend/
  go.mod
  go.sum
  Dockerfile
  cd deploy
docker build -f Dockerfile .
docker build -f deploy/Dockerfile .
