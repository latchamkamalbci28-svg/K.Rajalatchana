#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct package {
    char* id;
    int weight;
};

typedef struct package package;

struct post_office {
    int min_weight;
    int max_weight;
    package* packages;
    int packages_count;
};

typedef struct post_office post_office;

struct town {
    char* name;
    post_office* offices;
    int offices_count;
};

typedef struct town town;

void print_all_packages(town t) {
    printf("%s:\n", t.name);
    for (int i = 0; i < t.offices_count; i++) {
        printf("\t%d:\n", i);
        for (int j = 0; j < t.offices[i].packages_count; j++) {
            printf("\t\t%s\n", t.offices[i].packages[j].id);
        }
    }
}

void send_all_packages(town* source, int source_office_idx, town* target, int target_office_idx) {
    post_office* src = &(source->offices[source_office_idx]);
    post_office* tgt = &(target->offices[target_office_idx]);

    int accepted_count = 0;
    int rejected_count = 0;

    // Count accepted and rejected packages first
    for (int i = 0; i < src->packages_count; i++) {
        int w = src->packages[i].weight;
        if (w >= tgt->min_weight && w <= tgt->max_weight) {
            accepted_count++;
        } else {
            rejected_count++;
        }
    }

    // Allocate exact memory pools
    package* accepted_pkgs = malloc(accepted_count * sizeof(package));
    package* rejected_pkgs = malloc(rejected_count * sizeof(package));

    int a_idx = 0;
    int r_idx = 0;
    for (int i = 0; i < src->packages_count; i++) {
        int w = src->packages[i].weight;
        if (w >= tgt->min_weight && w <= tgt->max_weight) {
            accepted_pkgs[a_idx++] = src->packages[i];
        } else {
            rejected_pkgs[r_idx++] = src->packages[i];
        }
    }

    // Append accepted packages to target office tail
    if (accepted_count > 0) {
        tgt->packages = realloc(tgt->packages, (tgt->packages_count + accepted_count) * sizeof(package));
        for (int i = 0; i < accepted_count; i++) {
            tgt->packages[tgt->packages_count + i] = accepted_pkgs[i];
        }
        tgt->packages_count += accepted_count;
    }

    // Replace source office packages with only rejected packages
    free(src->packages);
    src->packages = rejected_pkgs;
    src->packages_count = rejected_count;

    // Clean up temporary tracking buffer
    free(accepted_pkgs);
}

town town_with_most_packages(town* towns, int towns_count) {
    int max_packages = -1;
    int target_idx = 0;

    for (int i = 0; i < towns_count; i++) {
        int current_packages = 0;
        for (int j = 0; j < towns[i].offices_count; j++) {
            current_packages += towns[i].offices[j].packages_count;
        }
        if (current_packages > max_packages) {
            max_packages = current_packages;
            target_idx = i;
        }
    }
    return towns[target_idx];
}

town* find_town(town* towns, int towns_count, char* name) {
    for (int i = 0; i < towns_count; i++) {
        if (strcmp(towns[i].name, name) == 0) {
            return &towns[i];
        }
    }
    return NULL;
}

int main() {
    int towns_count;
    if (scanf("%d", &towns_count) != 1) return 0;
    town* towns = malloc(towns_count * sizeof(town));
    for (int i = 0; i < towns_count; i++) {
        towns[i].name = malloc(16 * sizeof(char));
        scanf("%s", towns[i].name);
        scanf("%d", &towns[i].offices_count);
        towns[i].offices = malloc(towns[i].offices_count * sizeof(post_office));
        for (int j = 0; j < towns[i].offices_count; j++) {
            scanf("%d%d%d", &towns[i].offices[j].packages_count, &towns[i].offices[j].min_weight, &towns[i].offices[j].max_weight);
            towns[i].offices[j].packages = malloc(towns[i].offices[j].packages_count * sizeof(package));
            for (int k = 0; k < towns[i].offices[j].packages_count; k++) {
                towns[i].offices[j].packages[k].id = malloc(16 * sizeof(char));
                scanf("%s", towns[i].offices[j].packages[k].id);
                scanf("%d", &towns[i].offices[j].packages[k].weight);
            }
        }
    }
    int queries;
    if (scanf("%d", &queries) != 1) return 0;
    while (queries--) {
        int type;
        scanf("%d", &type);
        if (type == 1) {
            char name[16];
            scanf("%s", name);
            town* t = find_town(towns, towns_count, name);
            print_all_packages(*t);
        } else if (type == 2) {
            char source_name[16];
            char target_name[16];
            int source_office_idx;
            int target_office_idx;
            scanf("%s%d%s%d", source_name, &source_office_idx, target_name, &target_office_idx);
            town* source = find_town(towns, towns_count, source_name);
            town* target = find_town(towns, towns_count, target_name);
            send_all_packages(source, source_office_idx, target, target_office_idx);
        } else if (type == 3) {
            town m = town_with_most_packages(towns, towns_count);
            printf("Town with the most number of packages is %s\n", m.name);
        }
    }
    return 0;
}
