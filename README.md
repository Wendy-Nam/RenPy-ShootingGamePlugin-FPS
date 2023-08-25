# Shooting Game Plugin for Ren'Py (FPS)

Welcome to the Shooting Game Plugin for Ren'Py!

This plugin enables you to seamlessly integrate an immersive first-person shooting mini-game into your Ren'Py visual novel.

This readme provides a detailed guide on how to use the plugin, along with explanations and examples.

![image](https://img.itch.zone/aW1hZ2UvMjIwOTg2MC8xMzA2ODc4OS5wbmc=/original/pDDgi6.png)

## 🔫 Game Rules

In this first-person shooter game, players take on the role of a hunter. The game's key features include:

- Configurable gameplay elements, such as the number of targets per round, the number of rounds, time limits for each round, and the player's life count.

- The player's objective is to eliminate all targets within the time limit for each round.

- If a target isn't eliminated within the time limit, the player's life count decreases.

- The player can shoot targets by clicking the mouse.

## ✨ How to Use

1. <b>Integration</b>: To integrate the shooting game into your Ren'Py project, follow these steps:

   1. Copy the entire `hunt` directory into your project's root directory (`game/`).

   2. Add the following integration code to your script.rpy file where you want the game to start:

   ```renpy
   label start:
       "Hunting Game"
       window hide
       $ my_game_config = GameConfig(target_nb=4, time_limit=15, life_max=5, round_nb=4, bullet_max=20)
       $ hunt = HuntingGame(my_game_config)
       $ hunt.run()
       scene black
       "Finish Hunting"
   ```

   Make sure to adjust the `GameConfig` parameters as needed.

2. <b>Customization</b>

   - The game's behavior can be customized using the `GameConfig` class in the provided code.
   - You can adjust settings such as target image names, paths, numbers, time limits, life count, and more.

3. <b>Replacing Default Images</b>

   - The plugin uses default images for elements like bullets, crosshairs, weapons, and hearts.
   - To replace these images:

   1. Swap the default images in the `hunt/imgs` directory with your own images, ensuring they have the same dimensions and formats.

   2. Update the image paths in the `GameConfig` class accordingly.
      - For example, if you replace the bullet image, update the `IMG_BULLET` and `IMG_BULLET_EMPTY` paths in the `GameConfig` class.

## 👀 Example Usage

Suppose you want to create a shooting game with different parameters:

- Targets: 6
- Time limit: 20 seconds
- Life count: 3
- Rounds: 5
- Maximum bullets: 25
- Custom target image folder: `images/custom_targets/`
- Custom target image base name: `custom_target_`

Here's how you can achieve this:

```renpy
label start:
    "Hunting Game"
    window hide
    $ custom*game_config = GameConfig(target_img_path="images/custom_targets/", target_img_name='custom_target_', target_nb=6, time_limit=20, life_max=3, round_nb=5, bullet_max=25)
    $ hunt = HuntingGame(custom_game_config)
    $ hunt.run()
    scene black
    "Finish Hunting"
```

## 🚨 Note

To ensure proper functionality, adhere to the following:

- Each `target image's name` should be followed by <b>sequential numbers</b>, starting from 0.
- Place the directories containing target images under the `images` folder.

Enjoy creating an engaging shooting mini-game for your Ren'Py visual novel! If you have questions or need assistance, feel free to reach out.

## License

This Shooting Game Plugin for Ren'Py is provided under the `CC0 1.0 Universal` (CC0 1.0) Public Domain Dedication license. You can find a copy of the license in the [LICENSE](LICENSE) file.

This means you are free to use, modify, and distribute the plugin for any purpose, even commercially, without requiring attribution.

## 🎖️ Image Credits

- Crosshair: [Link](https://github.com/ColoradoStark/Renpy_Shooter/tree/master/game/hunt)
- Bullet: [Link](https://www.flaticon.com/free-icon/bullet_942477)
- Gun: [Link](https://www.pngwing.com/en/free-png-pbhhx)
- Targets: [Link](https://luizmelo.itch.io/monsters-creatures-fantasy)
- Heart: [Link](https://creazilla-store.fra1.digitaloceanspaces.com/emojis/56085/heart-suit-emoji-clipart-md.png)
