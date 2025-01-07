Rails.application.routes.draw do
  resources :questions do
    collection do
      post 'finish'
    end
  end
  resources :choices
  root 'questions#index'
end
