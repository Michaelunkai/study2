class CreateQuestions < ActiveRecord::Migration[7.1]
  def change
    create_table :questions do |t|
      t.text :content
      t.text :hint
      t.text :correct_answer

      t.timestamps
    end
  end
end
