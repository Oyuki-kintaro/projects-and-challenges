# Logical to Phyisical Memory Address Translation

1. Run make command
2. usage example:  ./translate addresses1 addresses1.output


The reference computing system for this assignment has the following properties: 1K physical memory, 4K virtual memory, and 128 bytes per page and frame.

Here is a program that takes in only two parameters, an infile, which is a file containing logical memory accesses, and the outfile, which output is written to. 

Each logical address in the infile is saved as 8 bytes (unsigned long) in binary format. The program reads logical addresses and then translates it into 
corresponding physical addresses based on the pagetable data given above. Each logical address in the sequence file, you will use the pagetable given above to 
perform the address translation and generate a corresponding physical address
