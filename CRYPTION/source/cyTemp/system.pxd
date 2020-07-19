from libcpp.string cimport string

cdef bytes GetVfsFile(string filename)
cdef object OpenVfsFile(string filename)
