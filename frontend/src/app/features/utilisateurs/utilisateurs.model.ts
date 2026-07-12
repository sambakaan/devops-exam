import { TypeUtilisateur } from '../../core/models/user.model';

export interface Utilisateur {
  id: string;
  nom: string;
  prenom: string;
  email: string;
  type_utilisateur: TypeUtilisateur;
  date_creation: string;
}

export const TYPES_UTILISATEUR: TypeUtilisateur[] = ['etudiant', 'professeur', 'personnel_administratif'];
