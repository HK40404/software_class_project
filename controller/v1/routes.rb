Rails.application.routes.draw do
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  get "test/search"
  post "test/result"
  get "test/assessment"
  get  "/test/personaltable"
end
