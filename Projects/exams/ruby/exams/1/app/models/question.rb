class Question < ApplicationRecord
  has_many :choices, dependent: :destroy
end
