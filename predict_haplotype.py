import sys
from collections import Counter 
from collections import OrderedDict

def get_haplotype_candidate(curr_genotypes):
		temp = []
		def dfs(curr, genotypes):
				if not genotypes:
						temp.append(curr[:])
						return 
				if genotypes[0] == "1":
						dfs(curr+"0",genotypes[1:])
						dfs(curr+"1",genotypes[1:])
				elif genotypes[0] == "2":
						dfs(curr+"1",genotypes[1:])
				elif genotypes[0] == "0":
						dfs(curr+"0",genotypes[1:])
		dfs("", curr_genotypes)
		return temp

def make_pair(curr_genotypes, candidate):
		temp = ""
		for i in range(len(curr_genotypes)):
				temp += str(int(curr_genotypes[i]) - int(candidate[i]))
		return temp

def E_step(curr_haplotype, prob):
		for curr in curr_haplotype:
				curr_sum = 0
				for i in range(len(curr_haplotype[curr])):
						left, right, curr_prob = curr_haplotype[curr][i]
						curr_prob = prob[left] * prob[right]
						curr_sum += curr_prob
						curr_haplotype[curr][i] = (left, right, curr_prob)

				for i in range(len(curr_haplotype[curr])):
						left, right, curr_prob = curr_haplotype[curr][i]
						if curr_sum  != 0:
								curr_haplotype[curr][i] = (left, right, curr_prob/curr_sum) 
						else:
								curr_haplotype[curr][i] = (left, right, 0)
		return curr_haplotype

def M_step(curr_haplotype, prob):
		for i in prob:
				prob[i] = 0
		for curr in curr_haplotype:
				for i in range(len(curr_haplotype[curr])):
						left, right, curr_prob = curr_haplotype[curr][i]
						prob[left] += curr_prob / (len(curr_haplotype) * 2)
						prob[right] += curr_prob / (len(curr_haplotype) * 2)
		return prob

def output_sol(output_file, res):
		res = list(zip(*res))
		for i in range(len(res)):
				output_file.write(" ".join(res[i]) + "\n")

def start_EM(genotypes):

		i, res, pro_box, haplotype_box = 0, [], {}, OrderedDict()

		for curr_genotypes in genotypes:
				temp, my_set = [], set()
				candidate = get_haplotype_candidate(curr_genotypes)
				for cp in candidate:
						curr_cp = make_pair(curr_genotypes, cp)
						if (curr_cp, cp) in my_set or (cp, curr_cp) in my_set:
								continue
						my_set.add((curr_cp, cp))
						temp.append((cp, curr_cp, 0.0))
						pro_box[curr_cp] = 0
						pro_box[cp] = 0
				haplotype_box[curr_genotypes+str(i)] = temp
				i += 1

		for key in pro_box:
				pro_box[key] = 1.0 / len(pro_box)

		EM_factor, changes = 0.0001, 10
		time = 0
		#while changes > EM_factor:
		while time != 11:
				time += 1
				haplotype_box = E_step(haplotype_box, pro_box)
				pro_box = M_step(haplotype_box, pro_box)
				#changes = 0
				#new_haplotype_box = E_step(haplotype_box, pro_box)
				#new_pro_box = M_step(new_haplotype_box, pro_box)

				#for gen in new_pro_box:
						#changes += (abs(pro_box[gen] - new_pro_box[gen]))**2

				#pro_box = new_pro_box
				#haplotype_box = new_haplotype_box

		for i in haplotype_box:
				haplotype = haplotype_box[i]
				haplotype = max(haplotype, key = lambda x: x[2])
				res.append(haplotype[0])
				res.append(haplotype[1])
		
		return res

# -----------------------------------------masked to unmasked-----------------------------------------------------
def main():
		genotypes = []
		real_data = []
		candidate = ["0","2"]

		input_file = open(MASKED, "r")
		output_file= open(SOL,"w+")

		bagging, bad, counter, i = {}, 0 , 0, 0

		for line in  input_file.readlines():
			curr_line = line.split()
			bagging[i] = Counter(curr_line)
			genotypes.append(curr_line[:])
			i += 1

		for i in range(len(genotypes)):
			for j in range(len(genotypes[0])):
				if genotypes[i][j] == "*":
						genotypes[i][j] = max(candidate, key = lambda x : bagging[i][x])

# -----------------------------------------EM Prediction-----------------------------------------------------
		window_size = 16
		cc = len(genotypes) // window_size
		c = 0
		index = 0
		while index < len(genotypes):
				print(str(c)+ " / " + str(cc) + " --- Done")
				c += 1
				if index + window_size <= len(genotypes):
						curr_genotypes = genotypes[index: index + window_size]
						curr_genotypes = list(zip(*curr_genotypes))
						curr_genotypes = ["".join(i) for i in curr_genotypes]
						curr_res = start_EM(curr_genotypes)
						output_sol(output_file, curr_res)
						index += window_size
				else:
						curr_genotypes = genotypes[index:]
						curr_genotypes = list(zip(*curr_genotypes))
						curr_genotypes = ["".join(i) for i in curr_genotypes]
						curr_res = start_EM(curr_genotypes)
						output_sol(output_file, curr_res)
						break

		input_file.close()
		output_file.close()

if __name__ == "__main__":
		#curr_res = start_EM(["21110", "10001", "22221"])
		#print(curr_res)
		global MASKED
		global SOL
		if len(sys.argv) == 3:
				MASKED = sys.argv[1]
				SOL = sys.argv[2]
		main()