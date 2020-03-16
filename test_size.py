MASKED = "example_data_2_masked.txt"
SOL = "sol.txt"
def main():
		t1, t2 = [], []
		input_file = open(MASKED, "r")
		output_file= open(SOL,"r")
		for line in  input_file.readlines():
			curr_line = line.split()
			t2.append(curr_line[:])

		for line in  output_file.readlines():
			curr_line = line.split()
			t1.append(curr_line[:])
		
		print(len(t1), len(t2))
		input_file.close()
		output_file.close()
if __name__ == "__main__":
		main()