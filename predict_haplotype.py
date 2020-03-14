from collections import Counter 
MASKED = "example_data_1_masked.txt"
UNMASKED = "example_data_1.txt"
SOL = "UNMASKED.txt"

def main():
		genotypes = []
		real_data = []
		temp = []
		candidate = ["0","2"]
		input_file = open(MASKED, "r")
		true_data_file = open(UNMASKED, "r")
		output_file= open(SOL,"w+")

		bagging, bad, counter, i = {}, 0 , 0, 0

		for line in  input_file.readlines():
			curr_line = line.split()
			bagging[i] = Counter(curr_line)
			temp.append(curr_line[:])
			genotypes.append(curr_line[:])
			i += 1
		
		for line in  true_data_file.readlines():
			real_data.append(line.split())

		for i in range(len(genotypes)):
			for j in range(len(genotypes[0])):
				if genotypes[i][j] == "*":
					counter += 1
					genotypes[i][j] = max(candidate, key=lambda x : bagging[i][x])

		for i in range(len(genotypes)):
			for j in range(len(genotypes[0])):
				if genotypes[i][j] != real_data[i][j]:
					bad += 1
		for i in range(len(genotypes)):
				output_file.write(" ".join(genotypes[i]) + "\n")

		input_file.close()
		output_file.close()

if __name__ == "__main__":
		main()