MASKED = "example_data_1_masked.txt"
SOL = "sol.txt"

def main():
		genotypes = []
		input_file = open(MASKED, "r")
		output_file= open(SOL,"w+")
		
		for line in  input_file.readlines():
			genotypes.append(line.split())

		for i in range(len(genotypes)):
				output_file.write(" ".join(genotypes[i]) + "\n")

		input_file.close()
		output_file.close()


if __name__ == "__main__":
		main()