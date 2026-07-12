export interface Livre {
  id: string;
  titre: string;
  auteur: string;
  isbn: string;
  quantite_totale: number;
  quantite_disponible: number;
  date_ajout: string;
}

export interface LivreCreate {
  titre: string;
  auteur: string;
  isbn: string;
  quantite_totale: number;
}

export interface LivreUpdate {
  titre?: string;
  auteur?: string;
  isbn?: string;
  quantite_totale?: number;
  quantite_disponible?: number;
}
