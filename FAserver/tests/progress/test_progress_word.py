def test_progress_word(client, auth_headers):
   # получаем слово
   words = client.get("/words", headers=auth_headers).json()
   number = 10
   for word in words[:number]:
      word_id = word["id"]

      review_response = client.get(
         f"/review/progress/word/{word_id}",
         headers = auth_headers
      )

      assert review_response.status_code == 200

