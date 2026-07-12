export type StatutEmprunt = 'en_cours' | 'retourne' | 'en_retard';

export interface Emprunt {
  id: string;
  livre_id: string;
  utilisateur_id: string;
  date_emprunt: string;
  date_retour_prevue: string;
  date_retour_effective: string | null;
  statut: StatutEmprunt;
}

export interface EmpruntCreate {
  livre_id: string;
  utilisateur_id: string;
}
