import json
import random
from locust import (HttpUser, task, between, TaskSet)
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
BASE_URL = 'https://api.fankave.com'
HEADERS = {'Content-Type': 'application/json', 'clientapikey': 'K5MeJJ3eQmZWt52K'}

token_list = ['eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ3OTc5OCwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDc5Nzk4LCJleHAiOjE2MTY0ODMzOTgsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.gQMYHPxnsYMhJkl400bxNWaR9JcvaPfmgC0xMpLpcsj9L9SeIwYzyjxV_crKcutroXGPRWaFssEO-qgL2S0_Z1C3OmS7YophLZlJA_tcOcIrTWjVs6WKGowSsrI2lk8hc1xXQ99HWvkbQWJpiRXI0_QZGwrY8zEGxkYcu2fzcWe5ULz0Da4vn0RNT23YmuvFaLeRRHxzyDLcJBTE7PUUmKipqYJeSut1TwBBVuOA4T9wgzGH3FQpdfiiSXpD2Hv-n_6XXCPGcpHXie9wX6vNkQivKzhB8efUpADs_5BNLoGDBVT8A5FdmPCsLy-kAkUiE9r9-xfKZn9n7Yf5MUHBiA',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDIxMSwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMjExLCJleHAiOjE2MTY0ODM4MTEsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.oxW_zLOe0X7X9PqQ0DlKfH-DUl5Hc7YBX_VUxTONiBcWPUcdpSjV27hKNiW99OPms3_32kjy8wHuqcrAQB5jpLtP8BRohbocEZk1qZFeQuB5vp3g8ZhPrUSrdp_JWGTAuxpKiC82qloIb7ci9bPcNrkM5UjO-aX8ZGQLEzKl7AdNu14GHUA0u6Z9ST0S-wW5JDVB4BDerhgQSRyYd9O_e7wGoxiVZ4zPcKRqqXlIJMquyYLrK0dqhEuIJo0QGky6dPWNZ34YLed4j8EU4ANGOGttWLsJZnc2bICV2KnoYiG9EVn6-9-b1frn7bUEA9ngsyWe7OzUV1nB6IYgfyNhzA',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDI1MCwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMjUwLCJleHAiOjE2MTY0ODM4NTAsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.HpFFY-BkwdIQ7J4Ak7lyj7LiRLyoF3-sQyR5qwsaitTpo8BJmpjrP2PLChv_VeroRYTVrQ9Hg2SVUdHWDuJGtkHeNT5LSnj2vXXWYmmWY9Uvp5EH83yTkpJWs4HQA2RfM0-kv151NcGwG3Ei_Nvx_a9VtJDOMGpr7RqSDisETxdroLnIs3_IWmSP9uMWNWJPRoHXDAwTMvkPmFD9jVQzXpbgrzhFmXdfx0U1Xg0doxIBmQ0ja1PrLTpyaXJZ8TyEKHM8Q7b7biUKyQPbAi11jOtF7UUphubnx2zHTn4YD5Jm59-Em2xCwzdZ0K6Tfi1jzncO6pABj5VPC_ArJZUdlg',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDI4MCwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMjgwLCJleHAiOjE2MTY0ODM4ODAsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.KSYKRzQw4mzJACfTY23Bnl3B3KVdlc7V8MkiNB0py8vAg9AEMfgjLMsdxvNMgvmh1jrKoOIw0hajmxea5CdgJOx6MU9Qpz1XXI-ja_paxyZAA7KW1yjaKCTBF7H1E1MIVq6X-KSaqNWf8YJpUPG1uRy8LjJ2F4CumXQ2fC89Po_zABR6bx8q_0q9L7LYf8YBFxaYExjo959Gr4bN7ewMu7JjiDIaFgyEoiIoRM9gmbMTomehkeA3tL6WsAwmhHoWp4j_DiMP9J4NsTgf_gfDl60akDQQ0t8fVEXh07NzGJJJFGbH-Jat3woqRPhnVpUM9enXb1Xa48nSNjYrD269cw',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDMxMiwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMzEyLCJleHAiOjE2MTY0ODM5MTIsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.KTsLFXFwSPMEpw1ReOsSg5L3lj5de29qXoJnPsg9f2Jk4x6-uuzckRvDmQVAQOfZ16tJeyHKpWNTm8iipYD8QIz5YEma1LO5knBkKmh-2v_VzyxKlrIPM9_YdVsuYkG1GytW75AwNEzbZBPsdZgAcQjQpm7JkqzcykfRrrxgq321mLhmuOZsZcyGZgdxx_rM6-AS2E6rAKA3kpDTWVNiSY7GMmgtxKk53hNu-o4FGpvExIOWMaesIyyRdcWVxzYD66SRfXH5NeVnpYhEvyaXKdBl51esg2LTwIBUvXrhAVZiCbeMdWhdVSACpYDYQOAjMGo4QmgpL1QhC1W0Flp8AQ',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDM0MiwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMzQyLCJleHAiOjE2MTY0ODM5NDIsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.gmOEz6CmAg1VIiYuZY7NNAv-F6lKOAkEqy7XDG1urGatERGMJyCNpBHyg-BwhC1pS5x6n9q2fY1nKXSXeGAq6kZ2uJ1h7H3TrWnVpJ7vmX1fyR0d9u5B3N9JM5HP6kRbjK3ns9GacVX_VUNjp46HCmPn3ex1r2KF84fYanP1LqatemW8NxDxsAodKJRGjFy7YVzGGb0AoI-6_18CIpZpVP_lG9UrBvQ4lUNOZAHOQQfWH7CqUFgDehOAUsDWsnmZvHJZWHgkocA3QZxb4LKSA5_xIQ0YF3eJ6weIONkjBB4k3MDtT22J7t-y5Pc8SQfRTOeVEt4NllpfhOcFgLX4hQ',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDM3MSwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwMzcxLCJleHAiOjE2MTY0ODM5NzEsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.S7A-GuDc_CJprzfot_Mln9QwayufrheYtY5QmYW9j2NQ9wp56C4J0LYU95cjx5-lHLfaBlvLS1zH1QSuuwDA47lbftkS8bZV3O46ll5ywY-2ud8i6MeyELksVApvWe5htSOQfQlzfOWTPvXAhcTg5RPer8tfB4lExzZxf-QDteJ7-RHLE-EoYgCkvazYZ7u_0pz5HMvNzhykHSPx89g1JDKgoOeOIABgQJwEzBh8HpscoBHs_HpqjrgkMSbX98WbESDCPoFNLZ-YyPdnsVNNajTMIIv2RhqqMeG8xwlFzuigeAjlpIW6PIbDqcoSZ_iw-d0QJdwHlg7-33CeFus9jg',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDQwNywidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwNDA3LCJleHAiOjE2MTY0ODQwMDcsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.HWxInRbN2ZeOE8foDEWIOvrFojiK289EG-i3n7ED_fLCA8lCv-2UtMh7_2T0HWgRd9Lc06IYhcX8FmdmVsttYV9uSLrzt3E-oDqc-oFWwPUcgffb5WFPWBlxMLFzhsNjqwvXSgkVkeEKxBU7Kzy0rwbJkLYvZcuHa_tdMeU4j7ushKvv4HT7tbjGTc2PVE2DY_XHRRAJZZ7y_whprbsVTp1cbtpSMKb83oAbA58EslYHAxGvwgj-qcmyAB2UedlJNXnhE95ObXU6q2h1GmPOw-sTCsXQLWjjrTyyGPuxQjaPz8qCbrTrZ7KT2myCqqZ-v34UOKDehOH-hSYvzLYmEA',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDQ4MywidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwNDgzLCJleHAiOjE2MTY0ODQwODMsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.VFWoC9QeEPArB2Z7FfaKgxE-S2OwEZCdk7x7LahjbAaWUG4BUCuQZE4ZBtVl3j6qu-14jsKDMssQQsroicEL0CFNR9b_-h1nEc58dmfjZ561a217c9IAoa4EbQYItZYA4NYUElHS0AOAoK25kgfiMett8476eRrbnJRnU-NobLnY3z4TT9pl4ZLAKkV6jyTKKWhJzFyFRwkn7Ik65a9ueGs4j9CYUYRG3wDht0BelprTpylEG126b3cJzRXpN5ghAQInaShwpYTqeyy2qmxGErvpbgcEsze8r7wbteAYO4Ke4_Suh8ElKW9F0qkSN9OplpmUhuq29rlXXbYgceNGKQ',
            'eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTXVoYW1tYWQgSW10aWF6IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdnWkE4TEF6TDJHWWF0Mko3NzhLMjZjRjFpZlJ0OU1NMVo1QU9rVz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vcHRpbXVtLXN1cmZhY2UtNjAyIiwiYXVkIjoib3B0aW11bS1zdXJmYWNlLTYwMiIsImF1dGhfdGltZSI6MTYxNjQ4MDU1NCwidXNlcl9pZCI6IndQN3JpYmRQbmlZRDNITW9yNHl6QUJUeUtsNzIiLCJzdWIiOiJ3UDdyaWJkUG5pWUQzSE1vcjR5ekFCVHlLbDcyIiwiaWF0IjoxNjE2NDgwNTU0LCJleHAiOjE2MTY0ODQxNTQsImVtYWlsIjoiaW10aWF6OTgzMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMzIzNDAyMDE5Nzc5NjgxMjU5MyJdLCJlbWFpbCI6WyJpbXRpYXo5ODMyQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.IH0wuFLgIFSV_kZQmmCTraFMsMJwNunGPLZoOQxjaA2bfQ3QCqPSc4SoTIS8tAthNDvGc3a6TlkRjlZ8qDtRbWOspIUBYFqwT_Oww7win0OnP4V-l8QTLTGrOuWH79Z-yoTicS-fi0M46rZTnFXg-VPLM4xCPJ4qY5lgAdnJsAIC3o0JF5GvC6HhA4H_yUOpkDELWWb5OAeLDEMJINSRbrHMWdoesbutgG0CoHEL5L1h_37l_ktXcEsE_garonJnLgR628GyFxr3refFel_-hjaw9dFMwsNlGjXPCBCq1M8s_Vj2q890hrQkG2pIbCDiRfa273dDbIp8zoTEp2neWQ']

# List to store tokens
list_size = 10
# token_list = []

def get_random_number_in_range():
    return random.randrange(0, list_size)

@task
def polling_verifytoken_api(self):
    # pick random token from list
    index = get_random_number_in_range()
    token = token_list[index]
    # print(token)
    with self.client.post(f'{BASE_URL}/ids/verifyRainfocus', headers=HEADERS, data=json.dumps({"token": f'{token}'}), catch_response=True) as response:
        #response_data = json.loads(response.content)
        #response_code = response_data['user']['responseCode']
        #print(response)
        if response.status_code != "0":
            return response.failure(f"Unable to verify Rainfoucs")

class IdsApp(HttpUser):
    wait_time = between(1, 2) #seconds
    tasks = [polling_verifytoken_api]
