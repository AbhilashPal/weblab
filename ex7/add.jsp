<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body bgcolor="red">
<%

int i = Integer.parseInt(req.getParameter("num1"));
int j = Integer.parseInt(req.getParameter("num2"));
int k = i+j;

out.println("Output : "+k);

%>
</body>
</html>