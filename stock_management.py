# importation module
from tkinter import messagebox
import mysql.connector
from tkinter import *

# -----------------------------------------------------------------

# création de ma fenêtre
screen = Tk()
screen.title("Boutique stock management")
screen.geometry("300x220")

# -----------------------------------------------------------------

# connexion à ma bdd
ma_bdd = mysql.connector.connect(
    user="root",
    password="root",
    database="boutique",
)

# -----------------------------------------------------------------

# résultat de la connexion àa ma bdd
if ma_bdd.is_connected():
    print("Connexion à la BDD réussie.")
else:
    print("Connexion à la BDD échoué.")

# -----------------------------------------------------------------

# widget Listbox pour l'affichage dans ma fenêtre
result_listbox = Listbox(screen)
result_listbox.place(x=10, y=40)

title = Label(screen, text="STOCK :", font=("arial", 15, "bold"), fg="black")
title.place(x=25, y=5)

# -----------------------------------------------------------------

# curseur d'éxecution de requête
boutique = ma_bdd.cursor()

# -----------------------------------------------------------------

# requête
boutique.execute("select * from produit")

# -----------------------------------------------------------------

# récupération des valeurs
resultat_stock = boutique.fetchall()

# -----------------------------------------------------------------

# affichage de mes valeurs
for resultat in resultat_stock:
    produit = resultat[0]  # récupère 1er élement donc l'id
    stock = resultat[1]  # récupère 2eme élement donc le nom
    result_listbox.insert(END, f"{produit}: {stock}")  # syntax Listbox


# -----------------------------------------------------------------

# fenêtre pour ajouter produit
def ajouter_produit():
    # Fonction appelée lors du clic sur le bouton "Ajouter un produit"
    fenetre = Toplevel(screen)
    fenetre.title("Ajouter un produit")
    fenetre.geometry("300x140")

    label_nom = Label(fenetre, text="Nom du produit :")
    label_nom.grid(row=0, column=0)
    champ_nom = Entry(fenetre)
    champ_nom.grid(row=0, column=1)

    label_description = Label(fenetre, text="Description :")
    label_description.grid(row=1, column=0)
    champ_description = Entry(fenetre)
    champ_description.grid(row=1, column=1)

    label_prix = Label(fenetre, text="Prix :")
    label_prix.grid(row=2, column=0)
    champ_prix = Entry(fenetre)
    champ_prix.grid(row=2, column=1)

    label_quantite = Label(fenetre, text="Quantité :")
    label_quantite.grid(row=3, column=0)
    champ_quantite = Entry(fenetre)
    champ_quantite.grid(row=3, column=1)

    label_categorie = Label(fenetre, text="ID catégorie :")
    label_categorie.grid(row=4, column=0)
    champ_categorie = Entry(fenetre)
    champ_categorie.grid(row=4, column=1)

    bouton_valider = Button(fenetre, text="Valider", command=lambda:
    enregistrer_produit(champ_nom.get(),
                        champ_description.get(),
                        champ_prix.get(),
                        champ_quantite.get(),
                        champ_categorie.get()))
    bouton_valider.grid(row=5, column=1)


# fonction d'enregistrement du produit
def enregistrer_produit(nom, description, prix, quantite, id_categorie):
    # création de mon cursor
    curseur = ma_bdd.cursor()

    # requête sql
    requete = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
    valeurs = (nom, description, prix, quantite, id_categorie)
    curseur.execute(requete, valeurs)

    ma_bdd.commit()

    # message validation
    messagebox.showinfo("Le produit a été ajouté avec succès")


# boutton ajouter produit
boutton_add = Button(screen, text="Ajouter un produit", command=ajouter_produit)
boutton_add.place(x=150, y=40, height=30, width=140)


# -----------------------------------------------------------------

# fenêtre pour supprimer un produit
def supp_produit():
    fenetre = Toplevel(screen)
    fenetre.title("Supprimer un produit")
    fenetre.geometry("300x50")

    label_nom = Label(fenetre, text="N°ID du produit à supprimer :")
    label_nom.grid(row=0, column=0)
    champ_nom = Entry(fenetre)
    champ_nom.grid(row=0, column=1)

    bouton_suppri = Button(fenetre, text="Supprimer", command=lambda: suppression(champ_nom.get()))
    bouton_suppri.grid(row=5, column=1)


def suppression(id):
    curseur = ma_bdd.cursor()

    requete = 'delete from produit where id = %s'
    valeur = (id,)
    curseur.execute(requete, valeur)

    ma_bdd.commit()

    messagebox.showinfo("Le produit a été supprimé avec succès")


boutton_del = Button(screen, text="Supprimer un produit", command=supp_produit)
boutton_del.place(x=150, y=80, height=30, width=140)

# -----------------------------------------------------------------

boutton_change = Button(screen, text="Modifier prix produit")
boutton_change.place(x=150, y=120, height=30, width=140)

boutton_stock = Button(screen, text="Modifier stock produit")
boutton_stock.place(x=150, y=160, height=30, width=140)

screen.mainloop()
