## Note: Each target image's name should be followed by sequential numbers, commencing from 0.
## Note : Make sure that the directories of target images should be placed under the images folder.
label start:
    # Create a specific game configuration instance
    "Hunting Game"
    window hide
    $ my_game_config1 = GameConfig(target_nb=4, time_limit=15, life_max=5, round_nb=4, bullet_max=20)
    # $ my_game_config2 = GameConfig(target_img_path="images/", target_img_name='t', target_nb=4, time_limit=15, life_max=5, round_nb=4, bullet_max=20)
    $ hunt = HuntingGame(my_game_config1)
    $ hunt.run()
    scene black
    "Finish Hunting"