package kr.ac.kpu.firstproject.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import kotlinx.android.synthetic.main.list_item.view.*
import kr.ac.kpu.firstproject.R

class BottomDialogAdapter(private val item: List<CNN_Result>, private val listener: OnItemClickListener) : RecyclerView.Adapter<BottomDialogAdapter.Holder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.list_item, parent, false)
        return Holder(view)
    }

    override fun getItemCount(): Int {
        return item.size
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val item = item[position]
        holder.result_tv.text = item.result
        holder.count_tv.text = item.count
    }

    inner class Holder(itemView: View) : RecyclerView.ViewHolder(itemView),
    View.OnClickListener{
        val result_tv: TextView = itemView.result_tv
        val count_tv: TextView = itemView.count_tv

        init{
            itemView.setOnClickListener(this)
        }

        override fun onClick(p0: View?) {
            val position = adapterPosition
            if(position != RecyclerView.NO_POSITION){
            listener.onItemClick(position)
                
            }

        }
    }

    interface OnItemClickListener{
        fun onItemClick(position: Int)
    }
}
