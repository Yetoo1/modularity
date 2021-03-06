#!/usr/bin/env python2.7
#By Scott Cohen
#There are no globals because I wanted to pass everything for the fun of it.
import os, sys, argparse, shutil
def dirf((cf,hf,l,sname,name,verbose,y,store,ll)):
	REQ = []; b = []
	lb = True; ln = True; it = False; id = False 
	for i,k in zip(l, range(0,len(l))):
		if i == [] and k == 1:
			lb = False
		if i == [] and k == 0:
			ln = False
	for i in range(0, len(name)):
		b.append(os.getcwd() + "/mod/" + name[i])
	a = os.getcwd() + "/mod/"		
	if not os.path.exists(a):
		if verbose:
			print "Mod directory doesn't exist.\nCreating it..."
		os.makedirs(a)
	try:
		for a, dirs, files in os.walk(a):
			if ln and a.split("/")[len(a.split("/"))-1] in l[0] or "?0" in l[0] and not a.split("/")[len(a.split("/"))-1] == "":
				print "Name: " + a.split("/")[len(a.split("/"))-1] + "\nPath: " + a
			if lb and a.split("/")[len(a.split("/"))-1] in l[1] or "?0" in l[1] and not a.split("/")[len(a.split("/"))-1] == "":
				print "Name: " + a.split("/")[len(a.split("/"))-1] + "\nPath: " + a
			if not a.split("/")[len(a.split("/"))-1][:1] == ".":
				for f in files:
					dir = a + "/" + f
					if a not in b and not all(n is None for n in name) == True: 
						break
 					elif dir[len(dir)-2:] == ".c":
                                		cf = dir + " " + cf
						if verbose:
							print cf
                        		elif dir[len(dir)-2:] == ".h":
                                		hf = hf + dir + " "
						if verbose:
							print hf
                        		elif dir[len(dir)-4:] == "info":
						if verbose:
							print dir
                                		try:
                                        		with open(dir, "r") as fo:
                                                		for line in fo:
								        if lb and "</DESC>" in line and not "#" in line:
										id = False 
									if "</INFO>" in line and not "#" in line:
                                                                		it = False
                                                        		if id:
										print line,
									if it:
                                                                		if "REQ=" in line and not "#" in line:
                                                                        		REQ.append((a.split("/")[len(a.split("/"))-1],line[4:len(line)-1]))
									if it:
										if "LIB=" in line and not "#" in line:
											for i in line.split(","):
												if "LIB=" in i:
													ll = ll + "-l" + i[4:len(line)-1]
												else:
													ll = ll + " -l" + i
									if lb:
										for i in l[1]:
											if i == a.split("/")[len(a.split("/"))-1] and "<DESC>" in line or i == "?0" and "<DESC>" in line:
												id = True
									if "<INFO>" in line and not "#" in line:
                                                                		it = True
                                                		fo.close()
                                		except IOError:
                                        		print "info doesn't exist."
                        		else:
                                		if verbose: 
                                        		print dir, "Not a good extension!"
                                		pass	
			else:
				if verbose:
					print "Skipping",a.split("/")[len(a.split("/"))-1]
		for i in range(0, len(REQ)):
                        if REQ[i][1] == "None" and not i == 0:
                                for t in range(0,len(REQ)-i):
                                        tmp = REQ[t]
                                        REQ[t] = REQ[t-1]
                                        REQ[t-1] = tmp
		i = 1
		try:
                	while(not i == 0):
                        	if len(REQ) == 1:
                                	if verbose:
						print "success", REQ[0]
					break
                        	if REQ[i][1] == REQ[i-1][0] and not REQ[i-1][0] == "None":
                                	if verbose:
                                        	print "success", REQ[i], REQ[i-1]
                                	i += 1
					if i == len(REQ):
						i = 0
                        	else:
                                	if verbose:
                                        	print "fail", REQ[i], REQ[i-1]
                                	tmp = REQ[i]
                                	REQ[i] = REQ[i+1]
                                	REQ[i+1]=tmp
                                	i = 1 #starts back at the beginning of the next check.
        	except IndexError:
                	print "ERROR:", REQ, "Incompatible Modules."
	except OSError:
		print "An error occured during the directory search."
	if (ln or lb) and not y:
		ask = raw_input("Do you want to continue?(y/n) ")
		if ask.lower() == "n":
			exit()
	return cf, hf, REQ, sname,verbose,y,store,ll
def cgen((c,h,REQ,sname,verbose,y,store,ll)): 
	asd = ""
	c = c.split(" ")
	h = h.split(" ")
	fo = open("a.c", "w")
	pt = ""
	for i in range(0, len(h) - 1): 
		fo.write("#include \"" + h[i] + "\"\n" + asd)
	fo.write("int main(){")
	for k in range(0, len(c) - 1):
		if (c[k][len(c[k])-3:] == "m.c"):	
			for x in range(0, len(REQ)):
				if c[k].split("/")[len(c[k].split("/"))-2] == REQ[x][0] and x == 0: 
					pt = pt + REQ[x][0] + "m()"
				if c[k].split("/")[len(c[k].split("/"))-2] == REQ[x][0] and x > 0:
					pt = REQ[x][0] + "m(" + pt + ")"
	fo.write(pt + ";}\n")
	fo.close()
	if verbose:
		print "Contents of 'a.c':",
		with open("a.c", "r") as fo:
			for line in fo:
				print line,
		fo.close()
	return " ".join(c),REQ,sname,verbose,y,store,ll
def com((c,REQ,sname,verbose,y,store,ll)): 
	a = ""
	if sname:
		a = sname
	else:
		for i in range(0, len(REQ)):
			a = a + REQ[i][0]
	if ll[3:] == "":
		ll = ll[3:]
	os.system("gcc " + c + "a.c -o " + a + " " + ll)
	if store:
		if verbose:
			print "Source:" + os.getcwd() + "/" + a, "\nDestination: " + store + "/" + a 
		try:
			shutil.move(os.getcwd() + "/" + a, store + "/" + a) 
		except IOError as e:
			print e, "\nCurrent directory will be used for storage instead."
	if verbose:
		print "\nDone."
	else:
		print "Done."
def get_args():
        p = argparse.ArgumentParser()
	p.add_argument("--version", "-V", help="Display the version.", 
			action="store_true")
        p.add_argument("--verbose", "-v", help="Enable verbose mode.",
                        action="store_true")
        p.add_argument("--modn", "-m", nargs="+", help="Change the modules to be selected.",
                        type=str)
	p.add_argument("--modl", "-lm", nargs="+", help="Lists the modules that exist as well as providing their respective info.",
			type=str)
        p.add_argument("--modl-info", "-i", nargs="+", help="Lists the module with info.",
			type=str)  
	p.add_argument("--name", "-n", nargs=1, help="Sets the name of the outputted executable. By default, the executable is all of the names in order combined.", 
			type=str)  
	p.add_argument("--yes", "-y", help="Passes yes to all confirmation prompts, try to make the checking mechanism that checks a value in a passed value for each switch so that one can pass yes or no for each part",
			action="store_true")
	p.add_argument("--store","-s", nargs=1, help="Input the full path of the destination to store the final executable. The default path will be in the directory this script is run.",
			type=str)
	p.add_argument("--link-library", "-ll", nargs="+", help="Input any libraries that may need to be required to proprly compile.",
			type=str)
	args = p.parse_args()
        return p.parse_args()
def run(args):
	a = []; b = []
	modname = "";
	store = ""
	llibrary = ""
	sname = ""
	if args.version:
		print "M%dularity 1.0"
	if args.verbose:
                print "Verbose mode enabled..."
	if args.modn:
		modname = " ".join(args.modn)
		print "Selecting:", modname
		modname = modname.split(" ")
	if args.modl_info:
		a = " ".join(args.modl_info)
		print "Listing info of: ", a
		a = a.split(" ")
	if args.modl:
		b = " ".join(args.modl)
		if "?0" not in args.modl:
			print "Listing:", b
		b = b.split(" ")
	if args.name:
		sname = args.name.pop()
	if args.store:
		store = args.store.pop()
	if args.link_library:
		llibrary = "-l" + " -l".join(args.link_library) + " "
	c = b, a
	return "","",c,sname,modname,args.verbose,args.yes,store,llibrary  
com(cgen(dirf(run(get_args()))))


