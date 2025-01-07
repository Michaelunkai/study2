json.extract! question, :id, :content, :hint, :correct_answer, :created_at, :updated_at
json.url question_url(question, format: :json)
