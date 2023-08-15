#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>


void translateAddresses(unsigned long* memAccesses, size_t numAddresses, int* page_table);

int main(int argc, char** argv) {
    // File variables
    char* inFile, *outFile;
    int input_file_descriptor, output_file_descriptor;
    struct stat st_in;
    size_t filesize;

    // Address variables
    unsigned long* memAccesses;
    int page_table[] = {2, 4, 1, 7, 3, 5, 6};
    size_t numAddresses;
    
    // Check for correct number of arguments
    if (argc != 3) {
        fprintf(stderr, "ERROR: Correct usage: %s infile outfile\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    inFile = argv[1];
    stat(inFile, &st_in);
    filesize = st_in.st_size;

    // Allocate space for all addresses
    memAccesses = (unsigned long*)malloc(filesize);

    // open and read input file
    input_file_descriptor = open(inFile, O_RDONLY);
    if (input_file_descriptor == -1) {
        perror("Input file open failed");
        free(memAccesses);
        exit(EXIT_FAILURE);
    }

    ssize_t bytesRead = read(input_file_descriptor, memAccesses, filesize);
	    if (bytesRead == -1) {
        perror("Error reading from file");
        close(input_file_descriptor);
        exit(EXIT_FAILURE);
    }
    close(input_file_descriptor);

    // open output file
    outFile = argv[2];
    output_file_descriptor = open(outFile, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (output_file_descriptor == -1) {
        perror("Output file open failed");
        free(memAccesses);
        close(input_file_descriptor);
        exit(EXIT_FAILURE);
    }

    // Perform address translation
	numAddresses = filesize / sizeof(unsigned long);
    translateAddresses(memAccesses, numAddresses, page_table);
    

    // Write to and close output file
    ssize_t bytesWritten = write(output_file_descriptor, memAccesses, filesize);
	if (bytesWritten == -1) {
        perror("Error writing to file");
        close(output_file_descriptor);
        exit(EXIT_FAILURE);
    }
    close(output_file_descriptor);

    // Free dynamically allocated memory
    free(memAccesses);

    return 0;
}

void translateAddresses(unsigned long* memAccesses, size_t numAddresses, int* page_table) {
    int i, offset, page, frame;

    for (i = 0; i < numAddresses; i++) {
        // Calculate offset
        offset = memAccesses[i] & 0xFF;
        offset = (offset << 1) & 0xFF;

        // Calculate page and find the corresponding physical frame
        page = memAccesses[i] >> 7;
        frame = page_table[page];
        frame = (frame << 8) | offset;
        frame = frame >> 1;

        printf("Virtual address %#05lx -> physical address %#05x\n", memAccesses[i], frame);
        memAccesses[i] = frame;
    }
}