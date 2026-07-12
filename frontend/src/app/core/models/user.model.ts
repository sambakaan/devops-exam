export type TypeUtilisateur = 'etudiant' | 'professeur' | 'personnel_administratif';

export interface User {
  id: string;
  nom: string;
  prenom: string;
  email: string;
  type_utilisateur: TypeUtilisateur;
  date_creation: string;
}

export interface RegisterPayload {
  nom: string;
  prenom: string;
  email: string;
  mot_de_passe: string;
  type_utilisateur: TypeUtilisateur;
}

export interface LoginPayload {
  email: string;
  mot_de_passe: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
