#include <stdio.h>
#include <string.h>

void magical_function(char *password) {
    // Mot de passe pour accéder à la fonction magique
    const char correct_password[] = "open_sessaame";
    if (strcmp(password, correct_password) == 0) {
        FILE *file = fopen("flag.txt", "r");
        if (file == NULL) {
            printf("Error: Could not open flag.txt\n");
            return;
        }
        
        char flag[256];
        if (fgets(flag, sizeof(flag), file) != NULL) {
            // Enlever le retour à la ligne si présent
            flag[strcspn(flag, "\n")] = 0;
            printf("The flag is: %s\n", flag);
        } else {
            printf("Error: Could not read flag from file\n");
        }
        fclose(file);
    } else {
        printf("Access denied! Wrong password.\n");
    }
}

void normal_function() {
    printf("Nothing to see here.\n");
}

int main() {
    setbuf(stdout, NULL);
    char password[50];

    printf("Welcome to the challenge!\n");
    normal_function();

    // Demander le mot de passe
    printf("Enter the password to access the magical function: ");
    scanf("%49s", password);  // Limite la saisie à 49 caractères pour éviter le débordement

    magical_function(password);
    return 0;
}