'''
Given two groups of agents arbitrarily chosen for this implementation to be Applicants and Companies,
each containing n members. The gale-shapely algorithm finds a stable matching where no pair
(applicant, company) prefers each other over their assigned match.

As input, it takes the number of n applicants and companies, a list of n preference lists
for the applicants, where each list ranks the n companies in descending order of preference,
and a list of n preference lists for the companies, where each list ranks the n applicants in
descending order of preference.

This solution is a greedy solution and is guaranteed to find a stable matching in O(n^2) worst
case time complexity. It requires that the two preferences lists are both of size exactly n.

Example1
n = 3
a_pref = {1: [2, 1, 3],
          2: [1, 3, 2],
          3: [1, 2, 3]}
c_pref = {1: [2, 1, 3],
          2: [3, 1, 2],
          3: [1, 2, 3]}
solution (applicant_matches, company_matches) = ({1: 2, 2: 1, 3: 3}, {1: 2, 2: 1, 3: 3})

Example2
n = 2
a_pref = {1: [2, 1],
          2: [1, 2]}
c_pref = {1: [2, 1],
          2: [1, 2]}
solution (applicant_matches, company_matches) = ({1: 2, 2: 1}, {1: 2, 2: 1})

Example3
n = 6,
a_pref = {1: [2, 3, 4, 5, 6, 1],
          2: [3, 1, 5, 6, 4, 2],
          3: [1, 6, 2, 3, 4, 5],
          4: [5, 4, 3, 1, 2, 6],
          5: [4, 2, 1, 3, 5, 6],
          6: [2, 5, 4, 3, 6, 1]}
c_pref = {1: [5, 2, 3, 4, 6, 1],
          2: [3, 4, 1, 6, 5, 2],
          3: [1, 2, 4, 5, 3, 6],
          4: [2, 3, 5, 1, 6, 4],
          5: [4, 1, 2, 3, 5, 6],
          6: [1, 5, 3, 4, 2, 6]}
solution (applicant_matches, company_matches) = ({1: 2, 2: 3, 3: 1, 4: 5, 5: 4, 6: 6}, {1: 3, 2: 1, 3: 2, 4: 5, 5: 4, 6: 6})


Note
    In the implementation, the agents are represented as positive integer numbers which are
    repeated between the groups but unique within the groups. This is an applicant centric solution.
    The output consists of a tuple of two dictionaries, the first element in the tuple displays
    the applicant's as keys and their matched company as values, the second is reversed.
'''

def gale_shapley(n, applicant_pref, company_pref ):
    unmatched_companies = set();
    unmatched_applicants = set();

    attempted_match_with = [set()] * n

    for i in range(n):
        unmatched_companies.add(i + 1) #Initialize each company to be free
        unmatched_applicants.add(i + 1) #Initialize each appplicant to be free

    applicant_matches = {i + 1: -1 for i in range(n)} #Dictionary storing matched pairs (Keys will be applicants, and values their matched companies)
    company_matches = {i + 1: -1 for i in range(n)} #Dictionary storing matched pairs (Keys will be companies, and values their matched applicants)

    while (len(unmatched_applicants) > 0):
        cur_a = unmatched_applicants.pop() #Pick a random unmatched applicant to start with
        cur_c = -1 #initialize cur_c variable to hold the current company being considered

        for company in applicant_pref[cur_a]:
            if company not in attempted_match_with[cur_a - 1]: #Pick the most preffered company thats not been matched with cur_a or hasnt tried to be matched
                cur_c = company
                break #Exit the loop since we picked one


        if (cur_c in unmatched_companies): #If the company is free (unmatched)
            applicant_matches[cur_a] = cur_c #Assign cur_c to cur_a
            company_matches[cur_c] = cur_a #Assign cur_c to cur_a
            unmatched_companies.remove(cur_c) #Reflect that the company has been matched

            attempted_match_with[cur_a - 1].add(cur_c) #Remember that we've tried to match with them before

        else:
            matched_preffered = False #O(1)
            #To see if the company prefers their matched applicant over cur_a
            for applicant in company_pref[cur_c]: #Iterate through the preference list of cur_c
                if applicant == cur_a: #This other applicant is actually preffered, keep the bool false
                    break
                elif applicant == company_matches[cur_c]:
                    matched_preffered = True #Recognie that their current match is preffered
                    break

            if matched_preffered:  #a rejects h
                unmatched_applicants.add(cur_a) #Add the applicant back into the pool, its not been able to be matched
                attempted_match_with[cur_a - 1].add(cur_c)  # Remember that we've tried to match with them before
                continue
            else: #So the new applicant is preffered by the company, we match them as follows
                unmatched_applicants.add(company_matches[cur_c]) #Add the applicant that was matched prior back into the unmatched pool
                applicant_matches[cur_a] = cur_c
                company_matches[cur_c] = cur_a
                unmatched_companies.remove(cur_c) #Reflect that the company has been matched

                attempted_match_with[cur_a - 1].add(cur_c) #Remember that weve tried to match with them before

    return (applicant_matches, company_matches)
