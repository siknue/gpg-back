# architech backend

## テストの実行

```shell
pytest
```

## 開発用サーバーの起動

```shell
uvicorn app.main:app --reload
```

## docker

lambda用のビルド

```shell
docker build --provenance=false -t architech-backend . 
```

lambdaテスト用サーバーの起動

```shell
 docker run -p 9000:8080 architech-backend  
```

lambda用のタグ付け

```shell
docker tag architech-backend:latest <aws account id>.dkr.ecr.ap-northeast-1.amazonaws.com/architech-backend:latest
```

ecrへアップロード

```shell
docker push <aws account id>.dkr.ecr.ap-northeast-1.amazonaws.com/architech-backend:latest
```
