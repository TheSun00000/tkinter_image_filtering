import tkinter as tk
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
import argparse

def resize_image(image, MAX=700):
    H, W = image.size
    if H > W:
        image = image.resize((MAX,W*MAX//H))
    else:
        image = image.resize((H*MAX//W,MAX))
    return image

def onkey(event):
    global img_id, n_saved

    if event.char in '12':
        
        if event.char == '2':
            # with open('space_gan_saved.txt', 'a') as file:
            with open(save_path, 'a') as file:
                file.write(f'{images[img_id]}\n')
                file.close()

            n_saved += 1
            saved_label.configure(text = f'Saved: {n_saved}')
            saved_label.text = f'Saved: {n_saved}'
            saved_label.pack(pady=20)
            print('Saved')
        elif event.char == '1':
            print('Deleted')

        img_id += 1
        image = Image.open(images_path+images[img_id])
        while image.size[0] < 400 and image.size[1] < 400:
            img_id += 1
            image = Image.open(images_path+images[img_id])

        image = resize_image(image)
        image = ImageTk.PhotoImage(image)
        label.configure(image = image)
        label.image = image
        label.pack()

        count_label.configure(text = f'{img_id}/{len(images)}')
        count_label.text = f'{img_id}/{len(images)}'
        count_label.pack(pady=20)


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', help="path of the dataset", type=str)
parser.add_argument('--clean', help="path in where to save the names of saved images", type=str)
parser.add_argument('--mh', help="minimum height of saved images", type=int, default=256)
parser.add_argument('--mw', help="minimum width of saved images", type=int, default=256)
args = parser.parse_args()
    

images_path = args.dataset
save_path = args.clean
min_H = args.mh
min_W = args.mw

img_id = 0
n_saved = 0

images = sorted(os.listdir(images_path))
print('[INFO] Dataset size =',len(images))

root = tk.Tk()
root.geometry('700x800')

image = Image.open(images_path+images[img_id])
image = resize_image(image)
image = ImageTk.PhotoImage(image)
label = tk.Label(root, image=image)
label.pack()

mybutton = tk.Button(root, text='PRESS ON TAB')
mybutton.bind("<Key>", onkey)
mybutton.pack(pady=20)

count_label = tk.Label(root, text=f'Count: 1/{len(images)}')
count_label.pack(pady=20)

saved_label = tk.Label(root, text=f'Saved: {n_saved}')
saved_label.pack(pady=20)

text_label = tk.Label(root, text='2:Save    1:Delete')
text_label.pack()


root.mainloop()
