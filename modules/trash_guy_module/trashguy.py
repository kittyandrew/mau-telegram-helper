# ============================================= #
#             Trash Guy Script                  #
#                 (> ^_^)>                      #
#          Made by Zac (t.me/Zacci)             #
#           Version 3.9.8.0286-pii              #
#      Donate:                                  #
#      1CoRm4mKCUPs5XQnFVSVQ4xGMAp29pyYzC       #
# ============================================= # =========================== #
# Copyright (C) 2019 Zac (https://t.me/Zacci)                                 #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the "Software"),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions: The    #
# above copyright notice and this permission notice shall be included in all  #
# copies or substantial portions of the Software.                             #
# =========================================================================== #
import sys


def main(user_input: str = '\U0001F353 \U0001F34A \U0001F345'):
    """Example usage of TrashGuy class."""
    trash_guy = TrashGuy(user_input, symbol_spacing=Symbols.SPACER_EMOJI)

    print(trash_guy)


class Symbols:
    SPACER_DEFAULT = '\u0020'
    SPACER_WIDE = '\u2800\u0020'
    SPACER_EMOJI = '➖'
    DEFAULT_INPUT = '\u2622'
    MONOSPACE_WRAPPER = '`'
    TRASH_EMOJI = '\U0001F5D1'
    GUY_LEFT = '<(^_^ <)'
    GUY_RIGHT = '(> ^_^)>'


class TrashGuy:
    def __init__(self, user_input: str = None,
                 symbol_trash: str = Symbols.TRASH_EMOJI,
                 symbol_left: str = Symbols.GUY_LEFT,
                 symbol_right: str = Symbols.GUY_RIGHT,
                 symbol_spacing: str = Symbols.SPACER_DEFAULT,
                 monospace_wrapper: str = Symbols.MONOSPACE_WRAPPER,
                 wrap_monospace: bool = False):
        if not user_input:
            self.user_input = [Symbols.DEFAULT_INPUT]
        else:
            self.user_input = str(user_input).split()

        self.symbol_trash = symbol_trash
        self.symbol_left = symbol_left
        self.symbol_right = symbol_right
        self.symbol_spacing = symbol_spacing
        self.monospace_wrapper = monospace_wrapper
        self.wrap_monospace = wrap_monospace

        self.item_index = 0
        self.frame_index = 2
        self.forward_indexing = True

    def __str__(self):
        return '\n'.join(frame for frame in self)

    def __iter__(self):
        return self

    def __wrap(self, canvas) -> str:
        wrapper = [Symbols.MONOSPACE_WRAPPER]
        if self.wrap_monospace:
            return ''.join(wrapper + list(canvas) + wrapper)
        else:
            return ''.join(list(canvas))

    def __next__(self):
        """Dynamically animated frames of trash guy using provided symbols."""
        trash_input = self.user_input

        s_trash = self.symbol_trash
        s_left = self.symbol_left
        s_right = self.symbol_right
        s_space = self.symbol_spacing

        item_index = self.item_index
        truncating_items = trash_input[item_index:]
        space_padding = [s_space] * item_index

        # Create a dynamic canvas while each item disappears
        canvas = [s_trash, *[s_space] * 3, *space_padding, *truncating_items]

        item_truncate_length = -len(truncating_items)
        last_index = len(canvas) - (-item_truncate_length)
        frame_index = self.frame_index
        if self.item_index < len(trash_input):
            # Start sequence, forward motion, going right
            if self.forward_indexing:
                if frame_index < last_index:
                    # Start from second space after the trash can
                    canvas[frame_index] = s_right

                    # Snapshot the frames of the animation going right
                    frame = self.__wrap(canvas)

                    # Remove this position from canvas for next frame
                    canvas[frame_index] = s_space

                    # Increment to next frame/forward position
                    self.frame_index += 1

                    return frame

                else:  # End of forward motion, look left with item
                    # Set item position in front of trash guy
                    canvas[frame_index - 1] = canvas[last_index]
                    # Set position of trash guy where item was
                    canvas[frame_index] = s_left

                    # Snapshot frame looking across at trash can
                    frame = self.__wrap(canvas)

                    # Remove these positions from canvas for next frame
                    canvas[frame_index] = canvas[frame_index - 1] = s_space

                    # Indicate to start moving backwards/left
                    self.forward_indexing = False

                    return frame

            # Reverse motion, going left
            else:
                # Going left with item towards trash can
                if frame_index > 1:
                    canvas[frame_index - 1] = s_left

                    # Place item in front while not yet at the trash can
                    if canvas[frame_index - 2] != s_trash:
                        canvas[frame_index - 2] = canvas[last_index]

                    # Temporarily remove item from trash pile while holding it
                    canvas[last_index] = s_space

                    # Snapshot the frames of the animation going left
                    frame = self.__wrap(canvas)

                    # Remove these positions from canvas for next frame
                    canvas[frame_index - 1] = canvas[frame_index - 2] = s_space

                    # Increment to next frame/forward position
                    self.frame_index -= 1

                    return frame

                else:  # End of reverse motion, look right for one frame
                    canvas[frame_index] = s_right

                    # Temporarily remove item from canvas for last frame also
                    canvas[last_index] = s_space

                    # Snapshot the frame looking right
                    frame = self.__wrap(canvas)

                    # Remove this position from canvas for next loop
                    canvas[frame_index] = s_space

                    # Initiate for next item sequence
                    self.forward_indexing = True
                    self.frame_index = 2

                    # Next item to be ready for next cycle
                    self.item_index += 1

                    return frame

        else:  # Animation complete, but was called again
            raise StopIteration


if __name__ == '__main__':
    if sys.argv[1:]:
        main(' '.join(sys.argv[1:]))
    else:
        main()
