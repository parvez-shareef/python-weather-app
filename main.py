from weather_service import get_weather, get_forecast, save_history, view_history

while True:
    print("\n=========================")
    print("   WEATHER APPLICATION")
    print("=========================")
    print("1. Search Weather")
    print("2. View Search History")
    print("3. Exit")

    choice = int(input("\nChoose an option: "))
    if choice==1:

      while True:
         city = input("\nEnter your city name: ")

         print(f"\nSearching weather for {city}...\n")

         weather = get_weather(city)
         wet = get_forecast(city)

         print("-------------------------")
         print("     WEATHER REPORT")
         print("-------------------------")

         # Network Error
         if weather is False or wet is False:
          print("Your network connection is lost.")
          print("Please connect to the Internet.")

    # Invalid City
         elif weather is None or wet is None:
          print("City not found.")
          print("Please enter a valid city name.")

    # Success
         else:
          for key, value in weather.items():
             print(f"{key:<15} : {value}")
          save_history(weather)

          print("\n-------------------------")
          print("   NEXT 5 FORECASTS")
          print("-------------------------")

          for forecast in wet:
             for key, value in forecast.items():
                print(f"{key:<15} : {value}")
             print("-------------------------")
          search_again = input("Search again? ").strip().lower()

          if search_again == "yes":
              continue      # Continue the weather search loop

          elif search_again == "no":
              break         # Exit the weather search loop and return to the main menu

          else:
              print("Please enter yes or no.")
           
    elif choice==2:
      view_history()
    elif choice==3:
      print("THANKS FOR USING OUR WEATHER APP")
      exit()