def test_progress_summary(client, auth_headers):
   result = client.get("/review/progress/summary", headers=auth_headers)

   assert result.status_code == 200
   data = result.json()
   assert data["total_words"] > 2
   assert data["learned_words"] is not None
   assert data["success_rate"] is not None
